import requests
import os
import time
import cv2
from dotenv import load_dotenv, set_key

# def get_streaming_token(api_key: str):
#     token_url = "https://api.verkada.com/cameras/v1/footage/token"
#     expiration = 3600
#     headers = {"Content-Type": 'application/json', "x-api-key": api_key}
#     response = requests.get(f"{token_url}?expiration={expiration}", headers=headers)
#     return response.json()['jwt']
STREAM_TIME = 3600  # seconds
RESOLUTION = 'high_res'
ORG_ID = 'a3c31a05-62b0-4d33-be6a-a2a4098ceabe'
CAMERA_ID = '175da6ac-b1d3-4e2a-8166-9b72139f1d1f'


def get_new_jwt(streaming_api_key: str):
    token_url = "https://api.verkada.com/cameras/v1/footage/token"
    expiration = STREAM_TIME
    headers = {"Content-Type": 'application/json', "x-api-key": streaming_api_key}
    response = requests.get(f"{token_url}?expiration={expiration}", headers=headers)
    return response.json()['jwt']


def get_jwt(streaming_api_key: str):
    # returns jwt token after checking if you need to get a new one
    current_epoch_time = int(time.time())
    expiration_epoch_time = current_epoch_time + STREAM_TIME
    if (
            'JWT_EXPIRATION' not in os.environ
            or 'JWT' not in os.environ
            or current_epoch_time >= int(os.environ['JWT_EXPIRATION'])
    ):
        jwt = get_new_jwt(streaming_api_key)
        os.environ['JWT'] = jwt
        os.environ['JWT_EXPIRATION'] = str(expiration_epoch_time)
        set_key('.env', 'JWT', jwt)
        set_key('.env', 'JWT_EXPIRATION', str(expiration_epoch_time))
    else:
        jwt = os.environ['JWT']
    return jwt


def get_streaming_url(org_id: str, jwt: str, camera_id: str, start_time: int = 0,
                      end_time: int = 0, resolution: str = RESOLUTION):
    video_url = ("https://api.verkada.com/stream/cameras/v1/footage/stream"
                 "/stream.m3u8")
    return (f"{video_url}?jwt={jwt}&org_id={org_id}&camera_id={camera_id}"
            f"&start_time={start_time}&end_time={end_time}&resolution={resolution}")


def get_cv2_capture_object(streaming_api_key, org_id, camera_id):
    # return camera stream
    jwt = get_jwt(streaming_api_key)
    streaming_url = get_streaming_url(org_id=org_id, jwt=jwt, camera_id=camera_id)
    stream = cv2.VideoCapture(streaming_url)
    return stream


def main():
    load_dotenv(override=True)
    streaming_api_key = os.environ.get('VERKADA_STREAMING_API_KEY')
    stream = get_cv2_capture_object(streaming_api_key, ORG_ID, CAMERA_ID)
    print(stream)


if __name__ == '__main__':
    main()
