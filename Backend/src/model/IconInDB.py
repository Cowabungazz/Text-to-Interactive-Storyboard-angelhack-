from pydantic import BaseModel, Field
from src.model.Icon import Icon

class IconInDB(Icon):
    id: str = Field(alias="_id")
