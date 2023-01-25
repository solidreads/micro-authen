from fastapi import FastAPI, Body, Depends

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer

from app.model import PostSchema

app = FastAPI()

posts = [{
    "id": 1,
    "title": "My first post",
    "content": "This is my first post"
}]

users = []


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Hello World"}


@app.post("/posts", dependencies=[Depends(JWTBearer())],  tags=["posts"])
async def get_posts(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }


@app.get("/posts/{post_id}", tags=["posts"])
async def get_single_post(post_id: int) -> dict:
    if post_id > len(posts):
        return {"message": "Post not found"}

    for post in posts:
        if post["id"] == post_id:
            return {"data": post}


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