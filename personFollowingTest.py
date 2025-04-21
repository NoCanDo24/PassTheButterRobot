import objectDetection
import cv2

d = objectDetection.objectDetection(trackedObjects=["person"])

while True:
    try:
        detections, frame = d.getBoxes()



        if len(detections) > 0:  
            for i in range(len(detections)):
                positionX = detections[i].xmin + (detections[i].xmax - detections[i].xmin)/2
                positionY = detections[i].ymin + (detections[i].ymax - detections[i].ymin)/2

                cv2.rectangle(frame, (positionX - 10, positionY + 10), (positionX + 10, positionY - 10), (255,0,0), cv2.FILLED) # Draw white box to put label text in

                
                print(positionX, positionY)

        cv2.imshow('detection Results', frame)

    except KeyboardInterrupt:
        print("Program stopped")
        
        d.cap.stop()
        cv2.destroyAllWindows()
        
        break
