from typing import Dict
from pydantic import BaseModel
from src.model.IconPosition import IconPosition

class Icon(BaseModel):
    icon_id: str
    position: IconPosition
