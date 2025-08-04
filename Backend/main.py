import contextlib

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import \
    CORSMiddleware  # for the backend to allow requests from the frontend (REACT) of a dirrent origin (port   3000)
from pymongo import MongoClient
import src.routers.lessons as lessons
import src.routers.icons as icons

app = FastAPI()

origins = ['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI and MongoDB application"}

app.include_router(lessons.router)
app.include_router(icons.router)