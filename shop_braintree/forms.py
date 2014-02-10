import datetime

from django import forms
from django.utils.translation import ugettext as _

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in xrange(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

NUMBER_ATTRS = {'autocomplete': 'off', 'size': '20', 'data-encrypted-name': 'number'}
CVV_ATTRS = {'autocomplete': 'off', 'size': '4', 'data-encrypted-name': 'cvv'}


class CardForm(forms.Form):
    number = forms.CharField(label=_("Card number"), widget=forms.TextInput(attrs=NUMBER_ATTRS))
    cvv = forms.CharField(label=_("Security code (CVV)"), widget=forms.TextInput(attrs=CVV_ATTRS))
    month = forms.CharField(label=_("Expiration month"), widget=forms.Select(choices=MONTH_CHOICES))
    year = forms.CharField(label=_("Expiration year"), widget=forms.Select(choices=YEAR_CHOICES))