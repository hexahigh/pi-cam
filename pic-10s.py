import time
import picamera
import os
from datetime import datetime

with picamera.PiCamera() as camera:
    while True:
        timestamp = datetime.now()
        folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = "{}.jpg".format(timestamp.strftime("%H:%M:%S"))
        file_path = os.path.join(folder_path, file_name)
        camera.capture(file_path)
        time.sleep(10)
