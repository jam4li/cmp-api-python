from django.conf import settings
import requests
from django.http import JsonResponse


def create_invoice(amount):
    api_key = settings.TETHER_API_KEY
    url = settings.TETHER_GATEWAY_URL
    expire_time = settings.TETHER_EXPIRE_TIME
    password = settings.TETHER_PASSWORD

    body = {
        'api_key': api_key,
        'password': password,
        'expire_time': expire_time,
        'amount': amount,
        'notify_url': 'https://test.cloudminepro.com/api/trc20/notify/',
        'success_url': 'https://panel.cloudminepro.com/dashboard',
        'fail_url': 'https://panel.cloudminepro.com/dashboard',
    }

    headers = {
        'Accept': 'application/json',
    }

    response = requests.post(url, headers=headers, data=body)

    return response.json()
