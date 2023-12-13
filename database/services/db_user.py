from database.services.hash import Hasher
from fastapi import HTTPException,status
from database.schemas.schemas import UserCreate,UserUpdate
from sqlalchemy.orm.session import Session
from database.models.models import DBuser


def create_user(db: Session, request: UserCreate):
    new_user = DBuser(
        email=request.email,
        hashed_password=Hasher.get_password_hash(request.password),
        role=request.role ,
        user_id=None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
def get_all_posts_by_user(db: Session, user_id: int):
    user = db.query(DBuser).filter(DBuser.id == user_id).first()

    if not user:
        return None 

    return user.posts


def delete(email:str ,db:Session):
    post = db.query(DBuser).filter(DBuser.email == email).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post successfully deleted"}


def update_user(email: str, updated_user: UserUpdate, db: Session):
    user = db.query(DBuser).filter(DBuser.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if updated_user.email:
        user.email = updated_user.email

    if updated_user.password:
        user.hashed_password = Hasher.get_password_hash(updated_user.password)

    if updated_user.role:
        user.role = updated_user.role

    db.commit()
    db.refresh(user)
    return user
    

def user_role(email:str ,db:Session):
    user= db.query(DBuser).filter(DBuser.email==email).first()
    if user and user.role == "admin":
        return {"role": "admin"}
    else:
        return {"role": "user"}
    


def user_login(email: str, password: str, db: Session):
    user = db.query(DBuser).filter(DBuser.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    auth_password = Hasher.verify_password(password, user.hashed_password)

    if auth_password:
        return {"message": "Login successful"} 

    raise HTTPException(status_code=401, detail="Password is incorrect")