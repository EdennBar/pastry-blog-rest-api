from fastapi import HTTPException,status
from database.schemas.schemas import PostBase
from sqlalchemy.orm.session import Session
from database.models.models import DBpost,DBuser
import datetime


def create(db:Session,request:PostBase,owner_id:int):
    new_post = DBpost(
        image_url = request.image_url,
        title = request.title,
        content = request.content,
        creator = request.creator,
        timestamp = datetime.datetime.now() ,
        owner_id = owner_id   
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db:Session):
    return db.query(DBpost).all()

def delete(id:int ,db:Session):
    post = db.query(DBpost).filter(DBpost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post successfully deleted"}
    