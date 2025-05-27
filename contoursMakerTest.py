import cv2
from picamera2 import Picamera2, Preview
import numpy as np

cap = Picamera2()
#cap.start_preview(Preview.QTGL)
picamStarted = False

kernel = np.ones((3,3), np.uint8)

while True:
	try:
		if not picamStarted:
			cap.start()
			picamStarted = True
		
		image = cap.capture_array()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		blurred = cv2.GaussianBlur(gray, (5,5), 0)
		edges = cv2.Canny(blurred, 50, 150)
		edges = cv2.dilate(edges, kernel, iterations=2)
		edges = cv2.erode(edges, kernel, iterations=1)
		
		#_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
		#thresh = cv2.GaussianBlur(thresh, (5,5), 0)
		#thresh_dilated = cv2.dilate(thresh, kernel, iterations=1)
		
		
		contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
		
		
		for contour in contours:
			area = cv2.contourArea(contour)
			if area < 500:
				continue
			
			x,y,w,h = cv2.boundingRect(contour)
			cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
			
		cv2.imshow('Contours', image)

		cv2.waitKey(5)
			
	except KeyboardInterrupt:
		cap.close()
		cv2.destroyAllWindows()
		break
