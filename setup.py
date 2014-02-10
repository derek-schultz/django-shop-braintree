from setuptools import find_packages, setup
setup(name="django-shop-braintree",
      version="0.1",
      description="A Braintree payment backend for django-shop",
      author="Derek Schultz",
      author_email='derek@derekschultz.net',
      platforms=["any"],
      license="MIT",
      url="http://github.com/derek-schultz/django-shop-braintree",
      packages=find_packages(),
      install_requires=["django", "django-shop", "braintree", "south"],
      )
