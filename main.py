from fastapi import FastAPI

from database.database import Base, engine
from routers import post
from routers import user
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

Base.metadata.create_all(engine)

app.mount('/images',StaticFiles(directory='images'),name='images')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)