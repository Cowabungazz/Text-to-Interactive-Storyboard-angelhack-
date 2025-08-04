from typing import Dict
from pydantic import BaseModel

class Branching(BaseModel):
    decision_point: str
    next_scenes: Dict[str, int]
