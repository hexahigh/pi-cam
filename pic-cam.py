import time
from picamera2 import Picamera2
from libcamera import controls
import os
from datetime import datetime
import logging
import RPi.GPIO as GPIO

# Set up logging
logging.basicConfig(filename='picamera.log', level=logging.INFO, format='%(asctime)s %(message)s')

picam = Picamera2()
config = picam.create_still_configuration()
picam.set_controls({"ExposureTime": 1000, "AfMode": controls.AfModeEnum.Continuous})
picam.controls.ExposureTime = 1000
picam.configure(config)
picam.start()

GPIO.setmode(GPIO.BOARD)
button_pin = 10
led_pin = 12
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            timestamp = datetime.now()
            folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_name = "{}.jpg".format(timestamp.strftime("%H_%M_%S"))
            file_path = os.path.join(folder_path, file_name)
            picam.capture_file(file_path)
            logging.info('Captured image and saved to: {}'.format(file_path))
            print('Captured image and saved to: {}'.format(file_path))
            
            # Blink the LED
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pin, GPIO.LOW)
            
        time.sleep(0.1)  # Debounce
except KeyboardInterrupt:
    GPIO.cleanup()

picam.stop()