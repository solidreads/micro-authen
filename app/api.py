from fastapi import FastAPI, Body, Depends

from app.schema import UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer


app = FastAPI()

users = []


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.get("/", dependencies=[Depends(JWTBearer())], tags=["root"])
async def read_root():
    return {"message": "Hello World"}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
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