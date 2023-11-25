from pprint import *
from picamera2 import Picamera2

picam = Picamera2()
pprint(picam.sensor_modes)