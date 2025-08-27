from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class InferenceResult():
    annotated_image : Any
    labels : List[str]

class InferenceModel():
    name : str
    def predict(self,image) -> InferenceResult:
        raise NotImplementedError

