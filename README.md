# Django Payment Manager

![Tests](https://github.com/adamspd/django-appointment/actions/workflows/tests.yml/badge.svg)
![Published on PyPi](https://github.com/adamspd/django-appointment/actions/workflows/publish.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-payment-manager.svg)](https://badge.fury.io/py/django-payment-manager)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/adamspd/django-payment)](https://github.com/adamspd/django-payment/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/adamspd/django-payment)](https://github.com/adamspd/django-payment/commit/main)
[![GitHub issues](https://img.shields.io/github/issues/adamspd/django-payment)](https://github.com/adamspd/django-payment/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/adamspd/django-payment)](https://github.com/adamspd/django-payment/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/adamspd/django-payment)](https://github.com/adamspd/django-payment/graphs/contributors)

This is a Django payment application that allows you to easily integrate with PayPal to accept payments. This app is
designed to be flexible, allowing you to collect payments for any type of service or product.

## Installation

1. Add the following code inside the `<head>` tag of your `base.html` template:

```html

<head>
    <!-- other tags -->
    <title>My title</title>
    {% block scriptHead %}{% endblock %} <!-- this line must be added -->
</head>
```

To use the application, a model must be created with at least the following field :

1. Create a model in your Django application that includes at least the following fields:

```python
from django.db import models
from payment.utils import get_timestamp, generate_random_id


class InfoToPassToPaymentApplication(models.Model):
    id_request = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)

    # Add any other fields you want

    def save(self, *args, **kwargs):
        if self.id_request is None:
            self.id_request = f"{get_timestamp()}{generate_random_id()}"  # You must create this function or use another method to generate a unique id
        return super().save(*args, **kwargs)

    def get_id_request(self):
        return self.id_request

    def get_amount_to_pay(self):
        return self.amount

    def get_currency(self):
        return self.currency

    def set_paid_status(self, status: bool):
        self.is_paid = status

    def get_name(self):
        # return the name of the service or product
        pass

    def get_img_url(self):
        # return the url of the image of the service or product
        pass

    def get_user_name(self):
        # return the name of the user who is going to pay
        pass

    def get_user_email(self):
        # return the email of the user who is going to pay
        pass

```

This model should represent the information that you want to pass to the payment application. This can include details
about the service or product you're selling, as well as any other necessary information.

## Usage

With your model created, you can now integrate the payment app with your existing application. Add the following
settings to your Django project's settings.py file, adjusting the values as needed:

```python
# settings.py

INSTALLED_APPS = [
    # other apps
    'payment',
]
```

If need be, the url used as entry point to the application is `payment:payment_linked`.

```python
# settings.py

# payment settings
PAYMENT_PAYPAL_ENVIRONMENT = 'sandbox'  # or 'production'
PAYMENT_PAYPAL_CLIENT_ID = 'your_paypal_client_id'
PAYMENT_PAYPAL_CLIENT_SECRET = 'your_paypal_client_secret'

# fees
# if you want to apply the default PayPal fee, set the following to True or add the fee to your model
PAYMENT_APPLY_PAYPAL_FEES = False  # (2.90% + 0.35$ per transaction, if card 2.10% + 0.35$ as of 2023-05-06) default is False
PAYMENT_SPLIT_PAYPAL_FEES = False  # split the fees between you and the user (if PAYMENT_APPLY_PAYPAL_FEES = True)  default  is False
# if you want to apply your own percentage fees (can't have both)
PAYMENT_FEES = 0.03 if not PAYMENT_APPLY_PAYPAL_FEES else 0.00  # default is 0.00

# basic
PAYMENT_BASE_TEMPLATE = 'base_templates/base.html'  # or your own base template path
PAYMENT_WEBSITE_NAME = 'My Website'  # or your website name
PAYMENT_MODEL = 'your_app_name.InfoToPassToPaymentApplication'  # Replace with your app and model name
PAYMENT_REDIRECT_SUCCESS_URL = 'your_app_name:success_view_name'  # Replace with your app and success view name

# Additional to the default email settings
# if the following are not defined, the default templates are applied
DEFAULT_FROM_EMAIL = "webmaster@localhost"  # the default from email that you're using
DEFAULT_EMAIL_MESSAGE = None  # leave as None if you want to use the default message in the template
DEFAULT_EMAIL_PAYMENT_SUCCESS_TEMPLATE = 'template/emails/payment_success.html'  # an example of name
```

DEFAULT_EMAIL_MESSAGE is the default message that you want to send to the user, leave empty if you want to
add one directly in the template or if you want to use the default one in the template which is :

```python
link = request.build_absolute_uri(payment_info.get_absolute_url())
message = DEFAULT_EMAIL_MESSAGE or f"Thank you for your payment, it's been received and your booking is now confirmed" \
                                       f"You can view it by clicking <a href='{link}'>here</a> " \
                                       f"We're excited to have you on board! Your order # is {order_id}."
```

The following objects are passed to the email template :

```python
context = {
    'first_name': first_name,
    'company': PAYMENT_WEBSITE_NAME,
    "order_id": order_id,
    "payment_info": payment_info,
    'message': message,
    'current_year': datetime.datetime.now().year,
}
```

payment_info is an object that contains the following attributes :

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class PaymentInfo:
    order_id = models.CharField(max_length=255, unique=True)
    reference_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    
    linked_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    linked_object_id = models.PositiveIntegerField(null=True, blank=True)
    linked_object = GenericForeignKey('linked_object_type', 'linked_object_id')

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_order_id(self):
        return self.order_id

    def get_reference_id(self):
        return self.reference_id

    def get_amount(self):
        return self.amount

    def get_currency(self):
        return self.currency

    def get_status(self):
        return self.status

    def get_linked_object(self):
        return self.linked_object

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def get_total_amount(self):
        return self.amount + self.fee
    
    def get_fee(self):
        return self.fee

    def get_absolute_url(self):
        # implemented in the payment app
        pass
        
 ```

You can customize the message in the email by not using the object message and directly put your message in the
template or by adding a changing the default value of the message in the settings.

The attribute in the payment_info object can be used to display the information in your template.

Follow the instructions in the app's documentation to set up the required views.

Once everything is set up, you can start accepting payments through PayPal.