from typing import List
from pydantic import BaseModel
from src.model.Scene import Scene

class Lesson(BaseModel):
    lesson_id: int
    scenes: List[Scene]
    language: str
