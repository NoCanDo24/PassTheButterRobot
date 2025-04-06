import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2


class objectDetection:

    # Load the model into memory and get labemap
    model_path = "yolo/yolo11n_ncnn_model"

    model = YOLO(model_path, task='detect')
    labels = model.names

    source_type = 'picamera'
    picam_idx = 0


    # Parse user-specified display resolution
    resize = True
    resW = 854
    resH = 480

    # Load or initialize image source
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(main={"format": 'XRGB8888', "size": (resW, resH)}))
    cap.start()

    # Set bounding box colors (using the Tableu 10 color scheme)
    bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
                  (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]

    def __init__(self, trackedObjects=labels):
        self.trackedObjects = trackedObjects

    def getBoxes(self):
        
        resultArr = []

        # Load frame from image source
        frame_bgra = self.cap.capture_array()
        frame = cv2.cvtColor(np.copy(frame_bgra), cv2.COLOR_BGRA2BGR)
        if (frame is None):
            print('Unable to read frames from the Picamera. This indicates the camera is disconnected or not working. Exiting program.')
            return

        # Resize frame to desired display resolution
        if self.resize == True:
            frame = cv2.resize(frame,(self.resW, self.resH))

        # Run inference on frame
        results = self.model(frame, verbose=False)

        # Extract results
        detections = results[0].boxes

        # Initialize variable for basic object counting example
        object_count = 0
        # Go through each detection and get bbox coords, confidence, and class

        for i in range(len(detections)):
            if self.labels[int(detections[i].cls.item())] in self.trackedObjects:

            # Get bounding box coordinates
            # Ultralytics returns results in Tensor format, which have to be converted to a regular Python array
                xyxy_tensor = detections[i].xyxy.cpu() # Detections in Tensor format in CPU memory
                xyxy = xyxy_tensor.numpy().squeeze() # Convert tensors to Numpy array
                xmin, ymin, xmax, ymax = xyxy.astype(int) # Extract individual coordinates and convert to int

            # Get bounding box class ID and name
                classidx = int(detections[i].cls.item())
                classname = self.labels[classidx]

            # Get bounding box confidence
                conf = detections[i].conf.item()
                
                resultArr.append(detection(xmin, ymin, xmax, ymax, classname, conf))            
        return resultArr

class detection:
    def __init__(self, xmin, ymin, xmax, ymax, label, confidence):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.label = label
        self.confidence = confidence

d = objectDetection(trackedObjects=["person", "bowl"])

while True:
    try:
        box = d.getBoxes()
        if len(box) > 0:  print(box[0].label, box[0].xmin, box[0].xmax)
    except KeyboardInterrupt:
        print("Program stopped")
        break
