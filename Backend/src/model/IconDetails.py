from pydantic import BaseModel

class IconDetails(BaseModel):
    icon_id: str
    description: str
    image_path: str
