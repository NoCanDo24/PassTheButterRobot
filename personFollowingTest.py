import objectDetection
import cv2

d = objectDetection.objectDetection(trackedObjects=["person"])

while True:
    try:
        detections, frame = d.getBoxes()

        if len(detections) > 0:  
            for i in range(len(detections)):
                positionX = detections[i].xmin + (detections[i].xmax - detections[i].xmin)/2
                positionY = detections[i].ymin + (detections[i].ymax + detections[i].ymin)/2
                

                
                print(positionX, positionY)
    except KeyboardInterrupt:
        print("Program stopped")
        break
