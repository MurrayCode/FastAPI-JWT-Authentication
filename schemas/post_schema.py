import datetime as dt
import pydantic as pydantic

class _PostBase(pydantic.BaseModel):
    post_body: str

class PostCreate(_PostBase):
    pass

class Post(_PostBase):
    id: int
    user_id: int
    date_created: dt.datetime

    class Config:
        orm_mode = True
    