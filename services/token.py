import models as models
import schemas.user_schema as user_schema
import jwt as jwt

JWT_SECRET = "PLACEHOLDER"

async def create_token(user: models.User):
    user_object = user_schema.User.from_orm(user)
    user_dict = user_object.dict()
    del user_dict["date_created"]

    token = jwt.encode(user_dict, JWT_SECRET)
    return dict(access_token=token, token_type="bearer")