
from fastapi import APIRouter,Depends, File, UploadFile,HTTPException
from database.schemas.schemas import UserCreate,UserUpdate,PostDisplay,LoginCredentials
from sqlalchemy.orm import Session
from database.services import db_user
from database.database import get_db


router = APIRouter(prefix="/user",tags=["/user"])

@router.post('/')
def create(request: UserCreate, db:Session = Depends(get_db)):
    return db_user.create_user(db, request)

@router.get('/all')
def posts(db:Session = Depends(get_db)):
    return db_user.get_all_users(db)

@router.get('/{user_id}/posts', response_model=list[PostDisplay])
def get_all_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    posts = db_user.get_all_posts_by_user(db, user_id)

    if not posts:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found or has no posts")

    return posts

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete(id, db)

@router.patch('/{email}')
def update_user(email: str, request: UserUpdate, db: Session = Depends(get_db)):
    return db_user.update_user_by_email(email, request, db)


@router.post('/login')
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    email = credentials.email
    password = credentials.password
    return db_user.user_login(email, password, db)


@router.get('/role/{email}')
def get_user_role(email: str, db: Session =Depends(get_db)):
    return db_user.user_role(email, db)