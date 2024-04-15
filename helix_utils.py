import requests
import os
from dotenv import load_dotenv
import time


def add_event(api_key, event_type, camera_id, time_ms, count):
    """
    Add a new event to helix
    """
    # add event
    event_types = get_event_types(api_key)
    event_type_uid = None
    for et in event_types:
        if et['name'].lower() == event_type.lower():
            event_type_uid = et['event_type_uid']
            break
    if not event_type_uid:
        event_type_uid = add_event_type(api_key, event_type)

    url = "https://api.verkada.com/cameras/v1/video_tagging/event"
    payload = {
        "attributes": {"count": count},
        "flagged": False,
        "camera_id": camera_id,
        "event_type_uid": event_type_uid,
        "time_ms": time_ms
    }
    headers = {
        "content-type": "application/json",
        "x-api-key": api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


def add_event_type(api_key, event_type, schema=None):
    """
    Add a new helix event type and return its uid
    """
    if schema is None:
        schema = {}
    schema["count"] = "integer"
    url = "https://api.verkada.com/cameras/v1/video_tagging/event_type"
    payload = {
        "event_schema": schema,
        "name": event_type
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['event_type_uid']


def get_event_types(api_key):
    url = "https://api.verkada.com/cameras/v1/video_tagging/event_type"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()['event_types']


def main():
    CAMERA_ID = '8a945cc7-b6df-467a-a065-bd4c551ad36a'
    load_dotenv(override=True)
    api_key = os.environ.get('VERKADA_API_KEY')
    cur_epoch_time_ms = time.time() * 1000
    print(add_event(api_key, 'test', CAMERA_ID, cur_epoch_time_ms, count=1))


if __name__ == '__main__':
    main()
