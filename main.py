from typing import List
import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import services.database as db_services
import services.user as user_services
import services.post as post_services
import services.token as token_services
import schemas.user_schema as user_schema
import schemas.post_schema as post_schema

app = fastapi.FastAPI()

@app.post("/api/users")
async def create_user(user: user_schema.UserCreate, db: orm.Session = fastapi.Depends(db_services.get_db)):
    db_user = await user_services.get_user_by_email(email=user.email, db=db)

    if db_user:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    user = await user_services.create_user(user=user, db=db)
    return await token_services.create_token(user=user)

@app.post("/api/token")
async def generate_token(form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(), db: orm.Session = fastapi.Depends(db_services.get_db)):
    user = await user_services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise fastapi.HTTPException(
            status_code=401,
            detail = "Invalid Credentials"
        )
    return await token_services.create_token(user=user)

@app.get("/api/user/me", response_model = user_schema.User)
async def get_user(user: user_schema.User = fastapi.Depends(user_services.get_current_user)):
    return user

@app.post("/api/user-post", response_model=post_schema.Post)
async def create_post(
    post: post_schema.PostCreate,
    user: user_schema.User = fastapi.Depends(user_services.get_current_user),
    db: orm.Session = fastapi.Depends(db_services.get_db)
):
    return await post_services.create_post(user=user, db=db, post=post)

@app.get("/api/my-posts", response_model=List[post_schema.Post])
async def get_user_posts(
    user: user_schema.User = fastapi.Depends(user_services.get_current_user),
    db: orm.Session = fastapi.Depends(db_services.get_db)
):
    return await post_services.get_user_posts(user=user, db=db)

@app.get("/api/my-posts/{post_id}", response_model=List[post_schema.Post])
async def get_post(
    post_id, 
    user: user_schema.User = fastapi.Depends(user_services.get_current_user),
    db: orm.Session = fastapi.Depends(db_services.get_db)
):
    return await post_services.get_post_by_id(id=post_id, user=user, db=db)
