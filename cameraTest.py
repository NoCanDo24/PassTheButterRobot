from picamera2 import Picamera2, Preview
from time import sleep

picam = Picamera2()
picam.start_preview(Preview.QTGL)

picamStarted = False

pictureCount = 0
while True:
	try:
		if not picamStarted:
			picam.start()
		
		com = input("Type camera command: ") 
		if com.split(" ")[0] == "capture":
			picam.capture_file("servoAnglePhotos/" + com.split(" ")[1] + ".jpg")
			
	except KeyboardInterrupt:
		picam.close()
		break

