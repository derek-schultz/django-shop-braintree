from django.contrib.auth.models import User
from django.db import models


class BraintreeCustomer(models.Model):
    user = models.OneToOneField(User)
    customer_id = models.CharField(max_length=36)  # max length defined by Braintree