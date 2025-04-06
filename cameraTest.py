from picamera2 import Picamera2, Preview
from time import sleep

picam = Picamera2()
picam.start_preview(Preview.QTGL)
picam.start()
sleep(5)
picam.close()
