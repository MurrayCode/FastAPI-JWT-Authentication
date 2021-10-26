import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
import database as db
import datetime as dt

class User(db.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String, unique=False)
    email = sql.Column(sql.String, unique=True, Index=True)
    password = sql.Column(sql.String)
    date_created = sql.Column(sql.DateTime, default= dt.datetime.utcnow)

class Post(db.Base):
    pass