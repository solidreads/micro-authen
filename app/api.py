import os

from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from app.schema import UsuarioSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer

from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

users = []


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.get("/", dependencies=[Depends(JWTBearer())], tags=["root"])
async def read_root():
    return {"message": "Hello World"}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UsuarioSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
