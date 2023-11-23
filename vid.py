import time
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality, H264Encoder, Encoder
from picamera2.outputs import FfmpegOutput
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
config = picam.create_video_configuration()
encoder = H264Encoder()
picam.configure(config)

timestamp = datetime.now()
folder_path = os.path.join(str(timestamp.month), str(timestamp.day))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
file_name = "{}.mp4".format(timestamp.strftime("%H_%M_%S"))
file_path = os.path.join(folder_path, file_name)

output1 = FfmpegOutput(file_path)
output2 = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream/stream.m3u8")
encoder.output = [output1, output2]

try:
    print('Starting encoder...')
    picam.start_encoder(encoder, quality=Quality.HIGH)  # Quality parameter moved here
    print('Encoder started.')
    print('Starting camera...')
    picam.start()
    print('Camera started.')
    logging.info('Started recording video to: {}'.format(file_path))
    print('Started recording video to: {}'.format(file_path))
    print('Starting DASH stream...')
    output2.start()
    print('Started DASH stream.')
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    while True:
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    picam.stop()
    output2.stop()
    server_thread.join()
    logging.info('Stopped recording video.')
    print('Stopped recording video.')