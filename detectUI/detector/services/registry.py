from .YOLO import YoloModel
from .Vit import VitModel


Yolo = YoloModel()
Vit = VitModel()

inference_models = {
    'yolo': Yolo,
    'vit': Vit, 
}

