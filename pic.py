import time
from picamera2 import Picamera2
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='picamera.log', level=logging.INFO, format='%(asctime)s %(message)s')

picam = Picamera2()
config = picam.create_still_configuration()
picam.set_controls({"ExposureTime": 1000, "AfMode": controls.AfModeEnum.Continuous})
picam.controls.ExposureTime = 1000
picam.configure(config)
picam.start()

timestamp = datetime.now()
folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
if not os.path.exists(folder_path):
  os.makedirs(folder_path)
file_name = "{}.jpg".format(timestamp.strftime("%H_%M_%S"))
file_path = os.path.join(folder_path, file_name)
picam.capture_file(file_path)
logging.info('Captured image and saved to: {}'.format(file_path))
print('Captured image and saved to: {}'.format(file_path))

picam.stop()
