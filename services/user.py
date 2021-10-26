import schemas.user_schema as user_schema
import models.user as user_models
import email_validator as validate_email
import sqlalchemy.orm as orm
import fastapi as fastapi
import fastapi.security as security
import jwt as jwt
import services.database as database
import passlib.hash as hash

#TODO swap to env variable
JWT_SECRET = "PLACEHOLDER"

oauth2schema = security.OAuth2PasswordBearer("/api/token")


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(user_models.User).filter(user_models.User.email == email).first()

async def create_user(user: user_schema, db: orm.Session):
    try:
        valid = validate_email.validate_email(email = user.email)
        email = valid.email
        name = user.name
    except validate_email.EmailNotValidError:
        raise fastapi.HTTPException(status_code=404, detail="Please enter a correct email address")

    user_object = user_models.User(email = email, name = name, password = hash.bcrypt.hash(user.password))
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

async def get_current_user(db: orm.Session = fastapi.Depends(database.get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms = ["HS256"])
        user = db.query(user_models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Incorrect email or password")
    return user_schema.User.from_orm(user)