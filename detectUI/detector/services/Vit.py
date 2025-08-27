from .base import InferenceModel, InferenceResult


class VitModel(InferenceModel):
    def __init__(self) -> None:
        super().__init__()

    def predict(self, image) -> InferenceResult:
        return super().predict(image)
