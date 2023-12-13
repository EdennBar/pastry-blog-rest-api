from database.database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship


class DBpost(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    title = Column(String)
    content = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DBuser", back_populates="posts")

class DBuser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    user_id = Column(Integer, ForeignKey("users.id"))
    posts = relationship("DBpost", back_populates="owner")