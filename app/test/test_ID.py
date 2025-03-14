import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
import numpy as np
import os
print(os.getcwd())

def RGB(event, x, y, flags, param): 
    if event == cv2.EVENT_MOUSEMOVE: 
        point = [x, y]
        print(point)
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB) # RGB when mouse run
# Load COCO class names
with open("coco1.txt", "r") as f:
    class_names = f.read().splitlines()
# Load the model
model = YOLO(r"D:\SourceCode\ProGabage\Garbage_Recognition_System\model\best.pt")
# Open the video file (use video file or webcam, here using webcam) #test
# cap = cv2.VideoCapture("speed.mp4") #test
# cap = cv2.VideoCapture("m.avi")  #test
cap = cv2.VideoCapture(0)
count=0
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 2 != 0:
       continue

    frame = cv2.resize(frame, (1020, 500)) #change size  
    
    # Run YOLO tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True) 

    # Check 
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        #information of objects  
        boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs 
        track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs 
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score %
       
        for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
            c = class_names[class_id]
            x1, y1, x2, y2 = box
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) #box 
            cvzone.putTextRect(frame,f'{track_id}',(x1,y2),1,1) #id track 
            cvzone.putTextRect(frame,f'{c}',(x1,y1),1,1)  #id object

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
       break

# display window
cap.release()
cv2.destroyAllWindows()

