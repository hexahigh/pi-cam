import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='picamera.log', level=logging.INFO, format='%(asctime)s %(message)s')

picam = Picamera2()
config = picam.create_video_configuration()
encoder = MJPEGEncoder()
picam.configure(config)

timestamp = datetime.now()
folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
file_name = "{}.jpg".format(timestamp.strftime("%H_%M_%S"))
file_path = os.path.join(folder_path, file_name)

try:
    picam.start_recording(file_path, encoder=encoder, quality=Quality.HIGH)  # Quality parameter moved here
    logging.info('Started recording video to: {}'.format(file_path))
    print('Started recording video to: {}'.format(file_path))
    while True:
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    picam.stop_recording()
    logging.info('Stopped recording video.')
    print('Stopped recording video.')
