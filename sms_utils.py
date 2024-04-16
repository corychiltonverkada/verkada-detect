import requests


def send_sms(textbelt_api_key, phone_number, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone_number,
        'message': message,
        'key': textbelt_api_key,
    })
    return resp.json()
