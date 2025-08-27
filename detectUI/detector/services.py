from ultralytics import YOLO
import cv2


def detect():
    pass




model = YOLO("yolov8n.pt")
results = model.predict(source="test.jpg",verbose = False, conf = 0.25)
detect_layer = results[0].plot()
out = "tmp.jpg"

cv2.imwrite(out,detect_layer)
