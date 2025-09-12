from dataclasses import dataclass
from typing import List, Optional, Any
from PIL import Image
@dataclass
class InferenceResult():
    annotated_image : Optional[Image.Image]
    labels : List[List[str]]

class InferenceModel():
    name : str
    def detect(self,image) -> InferenceResult:
        raise NotImplementedError

