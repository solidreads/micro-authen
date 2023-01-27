import logging
import uuid

import bcrypt
from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from passlib.context import CryptContext


from app.schema import UsuarioSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer

from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["scrypt"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


users = []


@app.get("/ping")
def pong():
    logging.warning("pong")
    return {"ping": "pong!"}


@app.get("/", dependencies=[Depends(JWTBearer())], tags=["root"])
async def read_root():
    return {"message": "Hello World"}


@app.post("/user/signup", tags=["user"])
async def crear_usuario(db: Session = Depends(get_db), user: UsuarioSchema = Body(...)):

    hashed_password = pwd_context.encrypt(user.password)
    db_user = models.Usuario(
        id=uuid.uuid4(),
        nombre_usuario=user.nombre_usuario,
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    return {"message": "Usuario creado correctanmente"}


@app.post("/user/login", tags=["user"])
async def user_login(db: Session = Depends(get_db), user: UserLoginSchema = Body(...)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not pwd_context.verify(user.password, db_usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return signJWT(user.email)


@app.get("/user/perfil", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_perfil(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()
