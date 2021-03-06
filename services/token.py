import models.user as user_models
import schemas.user_schema as user_schema
import jwt as jwt

#TODO replace with env variable
JWT_SECRET = "PLACEHOLDER"

async def create_token(user: user_models.User):
    user_object = user_schema.User.from_orm(user)
    user_dict = user_object.dict()
    del user_dict["date_created"]

    token = jwt.encode(user_dict, JWT_SECRET)
    return dict(access_token=token, token_type="bearer")