import fastapi as fastapi
import fastapi.security as security
import database as db
import sqlalchemy.orm as orm
import jwt as jwt
import schemas.post_schema as post_schema
import schemas.user_schema as user_schema
import models as models
import email_validator as validate_email
import passlib.hash as hash

oauth2schema = security.OAuth2PasswordBearer("/api/token")

JWT_SECRET = "PLACEHOLDER"

def create_database():
    return db.Base.metadata.create_all(bind=db.engine)

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(user: user_schema, db: orm.Session):
    try:
        valid = validate_email.validate_email(email = user.email)
        email = valid.email
        name = user.name
    except validate_email.EmailNotValidError:
        raise fastapi.HTTPException(status_code=404, detail="Please enter a correct email address")

    user_object = models.User(email = email,name = name, password = hash.bcrypt.hash(user.password))
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object

async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not user.check_password(password):
        return False
    
    return user

async def create_token(user: models.User):
    user_object = user_schema.User.from_orm(user)
    user_dict = user_object.dict()
    del user_dict["date_created"]

    token = jwt.encode(user_dict, JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def get_current_user(db: orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms = ["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Incorrect email or password")
    return user_schema.User.from_orm(user)

async def create_post(user: user_schema.User, db: orm.Session, post: post_schema.PostCreate):
    post = models.Post(**post.dict(), user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_schema.Post.from_orm(post)

async def get_user_posts(user: user_schema.User, db: orm.Session):
    posts = db.query(models.Post).filter_by(user_id=user.id)
    return list(map(post_schema.Post.from_orm, posts))

