# ai/detect.py

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # keep lightweight model

def detect_objects(frame):
    results = model(frame)

    detected = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = model.names[cls]

        # 🎯 Only treat these as hazards
            if label in ["person", "car", "truck", "bus", "animal"] and conf > 0.5:
                detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.putText(frame, f"{label}", (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    return frame, detected