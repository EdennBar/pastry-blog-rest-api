import shutil
from fastapi import APIRouter,Depends, File, UploadFile,HTTPException,status
from database.schemas.schemas import PostBase,PostDisplay
from sqlalchemy.orm import Session
from database.services import db_post
from database.database import get_db
from fastapi.responses import FileResponse
import string
import random
from fastapi.responses import JSONResponse
from os.path import join, exists
import os
router = APIRouter(prefix="/post",tags=["/post"])

@router.post('/{id}')
def create(id: int, request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(db, request, id)


@router.get('/all')
def posts(db:Session = Depends(get_db)):
    return db_post.get_all(db)

@router.delete('/{id}')
def delete(id:int ,db:Session = Depends(get_db)):
    return db_post.delete(id, db)

import uuid
@router.post("/images/")
async def create_upload_file(file: UploadFile = File(...)):
    # Specify the destination folder
    destination_folder = '/Users/edenbar/Desktop/pastryBlog/images/'

    
    try:
        os.makedirs(destination_folder, exist_ok=True)
    except OSError as e:
        return JSONResponse(content={"error": f"Error creating folder: {e}"}, status_code=500)

    
    file.filename = f"{uuid.uuid4()}.jpg"
    
    
    file_location = os.path.join(destination_folder, file.filename)

    
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename}

@router.get("/images/{image_url}")
async def get_image_url(image_url: str):
    destination_folder = '/Users/edenbar/Desktop/pastryBlog/images/'
    image_path = join(destination_folder, image_url)
    if exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}