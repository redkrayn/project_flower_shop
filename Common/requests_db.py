import requests


def request_db_is_ready_cakes():
    response = requests.get('')
    response.raise_for_status()
    return response.json()


def request_db_to_post_users_data(payload_users_data):
    url = ''
    response = requests.post(url, json=payload_users_data)
    response.raise_for_status()


def request_db_to_post_order_list(payload_order):
    url = ''
    response = requests.post(url, data=payload_order)
    response.raise_for_status()
