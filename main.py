import cv2
import os
import time
from ultralytics import YOLO
from dotenv import load_dotenv
from verkada_stream_utils import get_cv2_capture_object
from collections import Counter
from helix_utils import add_event

ORG_ID = 'a3c31a05-62b0-4d33-be6a-a2a4098ceabe'
CAMERA_ID = '8a945cc7-b6df-467a-a065-bd4c551ad36a'
MODEL_NAME = 'yolov8n.pt'
CONF_THRESHOLD = 0.5


def main():
    load_dotenv(override=True)
    streaming_api_key = os.environ.get('VERKADA_STREAMING_API_KEY')
    api_key = os.environ.get('VERKADA_API_KEY')
    model = YOLO(f'models/{MODEL_NAME}')
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
            print(class_map[cls], cnt)
            cls_name = class_map[cls]
            add_event(api_key, cls_name, CAMERA_ID, cur_epoch_time_ms, cnt)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
