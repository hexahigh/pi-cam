import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality, H264Encoder, Encoder
from picamera2.outputs import FfmpegOutput, FileOutput
import os
from datetime import datetime
import logging
import http.server
import socketserver
import threading

# Set up logging
logging.basicConfig(filename='picamera.log', level=logging.INFO, format='%(asctime)s %(message)s')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def start_server():
    PORT = 2233
    Handler = MyHTTPRequestHandler
    web_dir = os.path.join(os.path.dirname(__file__), 'stream')  # change 'web' to your directory
    os.chdir(web_dir)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


picam = Picamera2()
# XRGB8888
config = picam.create_video_configuration(raw={"format": "XRGB8888"}, encode="raw")
encoder = Encoder()
picam.configure(config)

output = FileOutput("test")
encoder.output = output

try:
    print('Starting encoder...')
    picam.start_encoder(encoder, quality=Quality.HIGH)  # Quality parameter moved here
    print('Encoder started.')
    print('Starting DASH stream...')
    picam.start()
    print('Started DASH stream.')
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    while True:
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    picam.stop()
    server_thread.join()
    logging.info('Stopped recording video.')
    print('Stopped recording video.')