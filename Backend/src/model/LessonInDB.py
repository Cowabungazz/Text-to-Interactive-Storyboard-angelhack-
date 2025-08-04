from pydantic import BaseModel, Field
from src.model.Lesson import Lesson

class LessonInDB(Lesson):
    id: str = Field(alias="_id")
