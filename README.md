django-shop-braintree
=====================

A Braintree payment backend for django-shop

Installation
------------
```
$ python setup.py install
```

Unfortunately, you cannot `pip install django-shop-braintree` at this time, but hopefully in the near future!

Configuration
-------------
If you haven't already, perform the standard Braintree configuration by placing the following in your settings file.

```python
import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="use_your_merchant_id",
                                  public_key="use_your_public_key",
                                  private_key="use_your_private_key")
```

You probably want to use environment variables or something more secure than including the keys directly as strings.

Add the backend class to your `SHOP_PAYMENT_BACKENDS` tuple in your settings file.

```python
SHOP_PAYMENT_BACKENDS = (
    'shop_braintree.backends.BraintreeBackend',
)
```