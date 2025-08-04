from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from src.model.Lesson import Lesson
from src.model.LessonInDB import LessonInDB
from src.model.Icon import Icon
from src.model.IconInDB import IconInDB
from src.model.IconDetails import IconDetails
from bson import ObjectId
from typing import List

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.lessons_db
lessons_collection = database.get_collection("lessons")
icons_collection = database.get_collection("icons")

# Helper function to convert MongoDB document to Lesson model
def lesson_helper(lesson) -> LessonInDB:
    lesson['_id'] = str(lesson['_id'])
    lesson['lesson_id'] = int(lesson['lesson_id'])  # Ensure lesson_id is an integer
    return LessonInDB(**lesson)

def icon_helper(icon) -> IconInDB:
    icon['_id'] = str(icon['_id'])
    return IconInDB(**icon)

# CRUD functions for lessons
async def create_lesson(lesson: Lesson) -> LessonInDB:
    lesson_dict = lesson.dict()
    result = await lessons_collection.insert_one(lesson_dict)
    new_lesson = await lessons_collection.find_one({"_id": result.inserted_id})
    return lesson_helper(new_lesson)

async def get_lesson(lesson_id: int, language: str) -> LessonInDB:
    lesson = await lessons_collection.find_one({"lesson_id": lesson_id, "language": language})
    if lesson:
        return lesson_helper(lesson)

async def get_lessons() -> List[LessonInDB]:
    lessons = []
    async for lesson in lessons_collection.find():
        # Print the lesson document for debugging
        print("Lesson document from MongoDB:", lesson)
        lessons.append(lesson_helper(lesson))
    return lessons

async def update_lesson(id: str, lesson: Lesson) -> LessonInDB:
    lesson_dict = lesson.dict()
    await lessons_collection.update_one({"_id": ObjectId(id)}, {"$set": lesson_dict})
    updated_lesson = await lessons_collection.find_one({"_id": ObjectId(id)})
    return lesson_helper(updated_lesson)

async def delete_lesson(id: str):
    result = await lessons_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count

# CRUD functions for icons
async def create_icon(icon: IconDetails) -> IconInDB:
    icon_dict = icon.dict()
    result = await icons_collection.insert_one(icon_dict)
    new_icon = await icons_collection.find_one({"_id": result.inserted_id})
    return icon_helper(new_icon)

async def get_icon(icon_id: str) -> IconInDB:
    icon = await icons_collection.find_one({"icon_id": icon_id})
    if icon:
        return icon_helper(icon)

async def get_icons() -> List[IconInDB]:
    icons = []
    async for icon in icons_collection.find():
        icons.append(icon_helper(icon))
    return icons

async def update_icon(id: str, icon: IconDetails) -> IconInDB:
    icon_dict = icon.dict()
    await icons_collection.update_one({"_id": ObjectId(id)}, {"$set": icon_dict})
    updated_icon = await icons_collection.find_one({"_id": ObjectId(id)})
    return icon_helper(updated_icon)

async def delete_icon(id: str):
    result = await icons_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count