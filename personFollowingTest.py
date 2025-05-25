import objectDetection
import cv2

b = objectDetection.objectDetection(model_path="person_butter")
#p = objectDetection.objectDetection(model_path="coco")

while True:
    try:
        detections, frame = b.getBoxes()



        if len(detections) > 0:  
            for i in range(len(detections)):
                positionX = int(detections[i].xmin + (detections[i].xmax - detections[i].xmin)/2)
                positionY = int(detections[i].ymin + (detections[i].ymax - detections[i].ymin)/2)

                cv2.rectangle(frame, (positionX-10, positionY-10), (positionX+10, positionY+10), (255,0,0), cv2.FILLED)

                

        cv2.imshow('detection Results', frame)

    except KeyboardInterrupt:
        print("Program stopped")
        
        b.cap.stop()
        cv2.destroyAllWindows()
        
        break
