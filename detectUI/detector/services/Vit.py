from .base import InferenceModel, InferenceResult


class VitModel(InferenceModel):
    def __init__(self) -> None:
        super().__init__()

    def detect(self, image) -> InferenceResult:
        return super().predict(image)
