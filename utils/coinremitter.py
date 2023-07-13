from django.conf import settings
import requests
from django.http import JsonResponse


def create_invoice(amount):
    api_key = settings.TETHER_API_KEY
    gateway_url = settings.TETHER_GATEWAY_URL
    notify_url = settings.TETHER_NOTIFY_URL
    expire_time = settings.TETHER_EXPIRE_TIME
    password = settings.TETHER_PASSWORD

    body = {
        'api_key': api_key,
        'password': password,
        'expire_time': expire_time,
        'amount': amount,
        'notify_url': notify_url,
    }

    headers = {
        'Accept': 'application/json',
    }

    response = requests.post(gateway_url, headers=headers, data=body)

    return response.json()
