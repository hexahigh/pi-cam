import time
from picamera2 import Picamera2, Preview
import os
from datetime import datetime

picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)
picam.start_preview(Preview.QTGL)
picam.start()

while True:
    timestamp = datetime.now()
    folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = "{}.jpg".format(timestamp.strftime("%H_%M_%S"))
    file_path = os.path.join(folder_path, file_name)
    picam.capture_file(file_path)
    time.sleep(10)

picam.stop()
