import base64
import logging
import sys
from decimal import Decimal

import requests

from payment.settings import PAYMENT_APPLY_PAYPAL_FEES, PAYMENT_SPLIT_PAYPAL_FEES, PAYMENT_FEES

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# configure basicConfig with the formatter, log level, and handlers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG,
                    handlers=[logging.StreamHandler(sys.stdout)])


def get_paypal_access_token(client_id, client_secret, endpoint_url):
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth}",
    }
    response = requests.post(f"{endpoint_url}/v1/oauth2/token", data="grant_type=client_credentials", headers=headers)
    data = response.json()
    return data["access_token"]


def generate_client_token(access_token, endpoint_url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Language": "en_US",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{endpoint_url}/v1/identity/generate-token", headers=headers)
    data = response.json()
    return data["client_token"]


def calculate_fee(amount, payment_type='paypal'):
    fees = {
        'paypal': {
            'percentage': Decimal('0.029'),
            'fixed': Decimal('0.35')
        },
        'card': {
            'percentage': Decimal('0.021'),
            'fixed': Decimal('0.35')
        }
    }

    if payment_type not in fees:
        raise ValueError("Invalid payment type. Supported payment types are 'paypal' and 'card'.")

    percentage_fee = fees[payment_type]['percentage']
    fixed_fee = fees[payment_type]['fixed']

    fee_amount = amount * percentage_fee + fixed_fee

    if PAYMENT_APPLY_PAYPAL_FEES and not PAYMENT_SPLIT_PAYPAL_FEES:
        # Apply the fee to the amount
        return fee_amount
    elif PAYMENT_APPLY_PAYPAL_FEES and PAYMENT_SPLIT_PAYPAL_FEES:
        # Return the fee amount
        return fee_amount / 2
    else:
        if PAYMENT_FEES is not None and PAYMENT_FEES > 0:
            fee_amount = amount * Decimal(PAYMENT_FEES)
        else:
            fee_amount = Decimal('0.00')

    return fee_amount


def calculate_total_amount(amount, payment_type='paypal') -> str:
    fee_amount = calculate_fee(amount, payment_type)
    logger.info(f"Fee amount: {fee_amount}")
    total_amount = amount + fee_amount
    logger.info(f"Total amount: {total_amount}")
    # return decimal format
    return "{:.2f}".format(total_amount)


def get_payment_details(order_id, access_token, endpoint_url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Language": "en_US",
        "Content-Type": "application/json",
    }
    response = requests.get(f"{endpoint_url}/v2/checkout/orders/{order_id}", headers=headers)
    data = response.json()
    return data
