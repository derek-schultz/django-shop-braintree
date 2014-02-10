# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.exceptions import ImproperlyConfigured
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

import braintree

from shop.util.decorators import on_method, order_required

from shop_braintree.models import BraintreeCustomer
from shop_braintree.forms import CardForm


class BraintreeBackend(object):
    url_namespace = 'braintree'
    backend_name = _('Braintree')
    template = 'shop_braintree/card.html'

    def __init__(self, shop):
        self.shop = shop

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.braintree_payment_view, name='braintree'),
        )
        return urlpatterns

    @on_method(order_required)
    def braintree_payment_view(self, request):
        form = CardForm
        if request.POST:
            order = self.shop.get_order(request)
            order_id = self.shop.get_order_unique_id(order)
            amount = self.shop.get_order_total(order)
            amount_in_cents = str(int(amount * 100))
            submit_for_settlement = getattr(settings, 'BRAINTREE_SUBMIT_FOR_SETTLEMENT', True)

            form = CardForm(request.POST)
            if form.is_valid():

                result = braintree.Transaction.sale({
                    "amount": amount,
                    "credit_card": {
                        "number": form.cleaned_data["number"],
                        "cvv": form.cleaned_data["cvv"],
                        "expiration_month": form.cleaned_data["month"],
                        "expiration_year": form.cleaned_data["year"]
                    },
                    "options": {
                        "submit_for_settlement": submit_for_settlement,
                    }
                })

                # Do not send the encrypted data back to the browser in the event of failure
                form.data = {}

                if result.is_success:
                    self.shop.confirm_payment(order, amount_in_cents, result.transaction.id, self.backend_name)
                    return self.braintree_success_view(request)
                else:
                    # There is a new add_error method in 1.6, but we will use this for now
                    errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                    errors.append(result.message)

        if hasattr(settings, 'BRAINTREE_CSE_KEY'):
            cse_key = settings.BRAINTREE_CSE_KEY
        else:
            raise ImproperlyConfigured('You must set BRAINTREE_CSE_KEY in your configuration file.')

        context = {
            'form': form,
            'cse_key': cse_key,
        }
        return render(request, "shop_braintree/payment.html", context)

    @on_method(order_required)
    def braintree_success_view(self, request):
        return HttpResponseRedirect(self.shop.get_finished_url())