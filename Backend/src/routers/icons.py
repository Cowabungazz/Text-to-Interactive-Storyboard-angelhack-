from fastapi import APIRouter, HTTPException
from typing import List
from src.model.IconDetails import IconDetails
from src.model.IconInDB import IconInDB
from src.db.Lessons import (
    create_icon,
    get_icon,
    get_icons,
    update_icon,
    delete_icon
)

router = APIRouter()

@router.post("/icons/", response_model=IconInDB)
async def create_icon_endpoint(icon: IconDetails):
    new_icon = await create_icon(icon)
    return new_icon

@router.get("/icons/{icon_id}", response_model=IconInDB)
async def get_icon_endpoint(icon_id: str):
    icon = await get_icon(icon_id)
    if icon is None:
        raise HTTPException(status_code=404, detail="Icon not found")
    return icon

@router.get("/icons/", response_model=List[IconInDB])
async def get_icons_endpoint():
    icons = await get_icons()
    return icons

@router.put("/icons/{id}", response_model=IconInDB)
async def update_icon_endpoint(id: str, icon: IconDetails):
    updated_icon = await update_icon(id, icon)
    if updated_icon is None:
        raise HTTPException(status_code=404, detail="Icon not found")
    return updated_icon

@router.delete("/icons/{id}", response_model=dict)
async def delete_icon_endpoint(id: str):
    delete_count = await delete_icon(id)
    if delete_count == 0:
        raise HTTPException(status_code=404, detail="Icon not found")
    return {"message": "Icon deleted successfully"}
