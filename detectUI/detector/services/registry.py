from .YOLO import YoloModel
from .Vit import VitModel


InferenceModels = {
    'yolo': lambda: YoloModel(),
    'vit': lambda: VitModel(),
}

