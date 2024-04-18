import cv2
import os
import time
import datetime
from ultralytics import YOLO
from dotenv import load_dotenv
from verkada_stream_utils import get_cv2_capture_object
from collections import Counter
from helix_utils import add_event
from email_utils import send_email
from sms_utils import send_sms
from utils import print_file

############################################################
# USER INPUTS
############################################################
ORG_ID = '413c1d1a-d8d6-4ef6-9b2c-df18cd9acf8f'
CAMERA_ID = 'ee981666-d5c6-49af-8c64-66430afd07ad'
MODEL_NAME = 'guns-knives-3.pt'
CONF_THRESHOLD = 0.7
EMAIL = 'cory.chilton@verkada.com'
PHONE_NUMBER = '6503395381'
############################################################


def main():
    print_file('./assets/verkada-logo.txt')
    print('\nWELCOME TO VERKADA DETEKT!\n')
    load_dotenv(override=True)
    streaming_api_key = os.environ.get('VERKADA_STREAMING_API_KEY')
    api_key = os.environ.get('VERKADA_API_KEY')
    gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD')
    textbelt_api_key = os.environ.get('TEXTBELT_API_KEY')
    model = YOLO(f'models/{MODEL_NAME}')
    print('Class names: \n', model.names)
    classes_to_report = input('\nWhich classes would you like to be notified about (comma separated): ')
    classes_to_report = classes_to_report.split(',')
    classes_to_report = set([int(cls) for cls in classes_to_report])
    while True:
        stream = get_cv2_capture_object(streaming_api_key, ORG_ID, CAMERA_ID)
        ret, frame = stream.read()
        results = model.predict(conf=CONF_THRESHOLD, source=frame)
        cv2.imshow('Live Stream', results[0].plot())
        class_list = results[0].boxes.cls.tolist()
        class_list = [int(n) for n in class_list]
        class_count = Counter(class_list)
        class_map = results[0].names
        cur_epoch_time_ms = int(time.time() * 1000)
        for cls, cnt in class_count.items():
            if cls not in classes_to_report:
                continue
            cls_name = class_map[cls]
            add_event(api_key, cls_name, CAMERA_ID, cur_epoch_time_ms, cnt)
            subject = f'Verkada Detect Alert: {cls_name.title()} Detected!'
            body = (
                f'{cls_name[0].upper() + cls_name[1:].lower()} detected at '
                f'{datetime.datetime.now().strftime("%H:%M on %m/%d/%Y")}'
            )
            send_email(gmail_app_password, EMAIL, subject, body)
            print('Email sent successfully')
            message = f'Verkada Detect Alert:\n{body}'
            sms_resp = send_sms(textbelt_api_key, PHONE_NUMBER, message)
            print(f'Text sent successfully (texts remaining: {sms_resp['quotaRemaining']})')
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
