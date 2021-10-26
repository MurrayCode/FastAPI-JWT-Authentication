import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
from sqlalchemy.sql.schema import Index
import database as db
import datetime as dt

class User(db.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String, unique=False)
    email = sql.Column(sql.String, unique=True, index=True)
    password = sql.Column(sql.String)
    date_created = sql.Column(sql.DateTime, default= dt.datetime.utcnow)
    posts = orm.relationship("Post", back_populates="owner")

    def check_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)
class Post(db.Base):
    __tablename__ = "posts"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    post_body = sql.Column(sql.String, index=True)
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    owner = orm.relationship("User", back_populates="posts")