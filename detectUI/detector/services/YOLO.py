from ultralytics import YOLO
import cv2
from .base import InferenceModel, InferenceResult

class YoloModel(InferenceModel):

    name : str = 'yolo'

    def __init__(self):
        
        self.model = YOLO("yolov8n.pt")

    def detect(self,image, conf = 0.25) -> InferenceResult:
        results = self.model.predict(source = image, verbose = False, conf = conf)
        labels = []
        r = results[0].boxes
        if r is not None:
            for box in r:
                id = int(box.cls[0])
                label = self.model.names[id]
                conf = box.conf
                labels.append(f'{label} ({conf})')

        return InferenceResult(annotated_image=None, labels=labels)


