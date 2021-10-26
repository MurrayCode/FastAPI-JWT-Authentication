from typing import List
import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
from sqlalchemy.sql.functions import user
import services as services
import schemas.user_schema as user_schema
import schemas.post_schema as post_schema

app = fastapi.FastAPI()

@app.post("/api/users")
async def create_user(user: user_schema.UserCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.get_user_by_email(email=user.email, db=db)

    if db_user:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    user = await services.create_user(user=user, db=db)
    return await services.create_token(user=user)

@app.post("/api/token")
async def generate_token(form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(), db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise fastapi.HTTPException(
            status_code=401,
            detail = "Invalid Credentials"
        )
    return await services.create_token(user=user)

@app.get("/api/user/me", response_model = user_schema.User)
async def get_user(user: user_schema.User = fastapi.Depends(services.get_current_user)):
    return user

@app.post("/api/user-post", response_model=post_schema.Post)
async def create_post(
    post: post_schema.PostCreate,
    user: user_schema.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    return await services.create_post(user=user, db=db, post=post)

@app.get("/api/my-posts", response_model=List[post_schema.Post])
async def get_user_posts(
    user: user_schema.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    return await services.get_user_posts(user=user, db=db)

