import cv2
import os
from ultralytics import YOLO
from dotenv import load_dotenv
from verkada_stream_utils import get_cv2_capture_object

ORG_ID = 'a3c31a05-62b0-4d33-be6a-a2a4098ceabe'
CAMERA_ID = '8a945cc7-b6df-467a-a065-bd4c551ad36a'
CONF_THRESHOLD = 0.5


def main():
    load_dotenv(override=True)
    streaming_api_key = os.environ.get('VERKADA_STREAMING_API_KEY')
    stream = get_cv2_capture_object(streaming_api_key, ORG_ID, CAMERA_ID)
    model = YOLO('models/bear-bestv2.pt')

    while True:
        ret, frame = stream.read()
        results = model.predict(conf=CONF_THRESHOLD, source=frame)
        cv2.imshow('Live Stream', results[0].plot())
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
