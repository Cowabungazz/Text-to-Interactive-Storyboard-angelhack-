from typing import List
from pydantic import BaseModel
from src.model.Icon import Icon
from src.model.Branching import Branching

class Scene(BaseModel):
    scene_id: int
    text: str
    icons: List[Icon]
    branching: Branching
