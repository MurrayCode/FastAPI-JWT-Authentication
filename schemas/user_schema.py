import datetime as dt
import pydantic as pydantic

class _UserBase(pydantic.BaseModel):
    email: str
    name: str

class UserCreate(_UserBase):
    password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int
    date_created: dt.datetime

    class Config:
        orm_mode = True