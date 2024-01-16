from django.conf import settings
from django.conf.global_settings import DEFAULT_FROM_EMAIL

# payment settings
PAYMENT_PAYPAL_ENVIRONMENT = getattr(settings, 'PAYMENT_PAYPAL_ENVIRONMENT')
PAYMENT_PAYPAL_CLIENT_ID = getattr(settings, 'PAYMENT_PAYPAL_CLIENT_ID')
PAYMENT_PAYPAL_CLIENT_SECRET = getattr(settings, 'PAYMENT_PAYPAL_CLIENT_SECRET')

# fees
PAYMENT_APPLY_PAYPAL_FEES = getattr(settings, 'PAYMENT_APPLY_PAYPAL_FEES', False)
PAYMENT_SPLIT_PAYPAL_FEES = getattr(settings, 'PAYMENT_SPLIT_PAYPAL_FEES', False)
PAYMENT_FEES = getattr(settings, 'PAYMENT_FEES', 0.00)

# basic
PAYMENT_BASE_TEMPLATE = getattr(settings, 'PAYMENT_BASE_TEMPLATE', 'base_templates/base.html')
PAYMENT_WEBSITE_NAME = getattr(settings, 'PAYMENT_WEBSITE_NAME', 'Website')
PAYMENT_MODEL = getattr(settings, 'PAYMENT_MODEL')
PAYMENT_REDIRECT_SUCCESS_URL = getattr(settings, 'PAYMENT_REDIRECT_SUCCESS_URL')

# email
APP_DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
DEFAULT_EMAIL_MESSAGE = getattr(settings, 'DEFAULT_EMAIL_MESSAGE', None)
DEFAULT_EMAIL_PAYMENT_SUCCESS_TEMPLATE = getattr(settings, 'DEFAULT_EMAIL_PAYMENT_SUCCESS_TEMPLATE', None)
EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', '')
SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', None)
