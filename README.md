django-shop-braintree
=====================

A Braintree payment backend for django-shop

Installation
------------
Simply run
```
$ pip install django-shop-braintree
```

If you would prefer to install from source, just do
```
$ python setup.py install
```

Configuration
-------------
Start off by adding `shop_braintree` to your `INSTALLED_APPS`.


If you haven't already, perform the standard Braintree configuration by placing the following in your settings file.

```python
import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox,  # or Production
                                  merchant_id="use_your_merchant_id",
                                  public_key="use_your_public_key",
                                  private_key="use_your_private_key")
```

Also add a setting for your client side encryption key.

```python
BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY = 'use_your_cse_key'
```

You probably want to use environment variables or something more secure than including the keys directly as strings.

Add the backend class to your `SHOP_PAYMENT_BACKENDS` tuple in your settings file.

```python
SHOP_PAYMENT_BACKENDS = (
    'shop_braintree.backends.BraintreeBackend',
)
```

By default, the order is automatically submitted for settlement. If you want to disable this so that you can manually
submit for settlement through the Braintree admin when the order is ready to ship, then set this to false.

```python
BRAINTREE_SUBMIT_FOR_SETTLEMENT = False
```

Additional Setup
----------------
A `BraintreeCustomer` model keeps track of customer IDs. Therefore, you must run `./manage.py migrate` to sync up the
database.

Override the templates in `shop_braintree/templates` and customize them to your liking.

Helpful Hints
-------------
When payment is complete, the page redirects to `shop.get_finished_url()`, which calls `reverse` on
`'thank_you_for_your_order'`.
