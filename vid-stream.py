import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FfmpegOutput
import os
from datetime import datetime
import logging
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-k", "--key", help="stream key")

args = argParser.parse_args()

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
file_name = "{}.mjpg".format(timestamp.strftime("%H_%M_%S"))
file_path = os.path.join(folder_path, file_name)

# Create FfmpegOutput
output = FfmpegOutput("-f flv rtmp://a.rtmp.youtube.com/live2/" + args.key)

try:
    picam.start_recording(encoder, output=output, quality=Quality.HIGH)  # Quality parameter moved here
    logging.info('Started recording video to: {}'.format(file_path))
    print('Started recording video to: {}'.format(file_path))
    while True:
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    picam.stop_recording()
    logging.info('Stopped recording video.')
    print('Stopped recording video.')
