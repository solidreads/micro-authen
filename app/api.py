import logging
import uuid

import bcrypt
from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session

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
async def crear_usuario(db: Session = Depends(get_db), user: UsuarioSchema = Body(...)):

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    logging.warning(len(hashed_password))
    db_user = models.Usuario(
        id=uuid.uuid4(),
        nombre_usuario=user.nombre_usuario,
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully!"}


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Wrong login details!"}


@app.get("/user/perfil", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_perfil(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()
