from .base import InferenceModel, InferenceResult

class YoloModel(InferenceModel):
    def __init__(self):
        pass

    def predict(self,image) -> InferenceResult:
        return InferenceResult(None,['Label'])
