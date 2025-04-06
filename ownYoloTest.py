# for futur dumb Leo: to use file in command prompt first type: source venv/bin/activate
# then you can run the following command:
# python yolo_detect.py --model=yolo11n_ncnn_model --source=picamera0 --resolution=500x300
# I think you can figure out what it does (if not, first of all shame on you, after that watch this video again: https://www.youtube.com/watch?v=z70ZrSZNi-8)

import cv2
import numpy as np
from ultralytics import YOLO

# Define and parse user input arguments



# Load the model into memory and get labemap
model_path = "yolo/yolo11n_ncnn_model"

model = YOLO(model_path, task='detect')
labels = model.names

source_type = 'picamera'
picam_idx = 0


# Parse user-specified display resolution
resize = True
resW = 700
resH = 500

# Load or initialize image source
from picamera2 import Picamera2
cap = Picamera2()
cap.configure(cap.create_video_configuration(main={"format": 'XRGB8888', "size": (resW, resH)}))
cap.start()

# Set bounding box colors (using the Tableu 10 color scheme)
bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
              (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]

# Initialize control and status variables
img_count = 0

# Begin inference loop
while True:


    # Load frame from image source
    frame_bgra = cap.capture_array()
    frame = cv2.cvtColor(np.copy(frame_bgra), cv2.COLOR_BGRA2BGR)
    if (frame is None):
        print('Unable to read frames from the Picamera. This indicates the camera is disconnected or not working. Exiting program.')
        break

    # Resize frame to desired display resolution
    if resize == True:
        frame = cv2.resize(frame,(resW,resH))

    # Run inference on frame
    results = model(frame, verbose=False)

    # Extract results
    detections = results[0].boxes

    # Initialize variable for basic object counting example
    object_count = 0

    # Go through each detection and get bbox coords, confidence, and class
    for i in range(len(detections)):
        if labels[int(detections[i].cls.item())] != "":
            
        # Get bounding box coordinates
        # Ultralytics returns results in Tensor format, which have to be converted to a regular Python array
            xyxy_tensor = detections[i].xyxy.cpu() # Detections in Tensor format in CPU memory
            xyxy = xyxy_tensor.numpy().squeeze() # Convert tensors to Numpy array
            xmin, ymin, xmax, ymax = xyxy.astype(int) # Extract individual coordinates and convert to int

        # Get bounding box class ID and name
            classidx = int(detections[i].cls.item())
            classname = labels[classidx]

        # Get bounding box confidence
            conf = detections[i].conf.item()

        # Draw box if confidence threshold is high enough
            if conf > 0.5:

                color = bbox_colors[classidx % 10]
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2)

                label = f'{classname}: {int(conf*100)}%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # Draw label text

            # Basic example: count the number of objects in the image
                object_count = object_count + 1

    # Calculate and draw framerate (if using video, USB, or Picamera source)    
    # Display detection results
    cv2.putText(frame, f'Number of objects: {object_count}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2) # Draw total number of detected objects
    cv2.imshow('YOLO detection results',frame) # Display image

    # If inferencing on individual images, wait for user keypress before moving to next image. Otherwise, wait 5ms before moving to next frame.
    key = cv2.waitKey(5)
    
    if key == ord('q') or key == ord('Q'): # Press 'q' to quit
        break
    elif key == ord('s') or key == ord('S'): # Press 's' to pause inference
        cv2.waitKey()
    elif key == ord('p') or key == ord('P'): # Press 'p' to save a picture of results on this frame
        cv2.imwrite('capture.png',frame)
    

# Clean up
cap.stop()
cv2.destroyAllWindows()
