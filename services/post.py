import models.post as post_models
import schemas.user_schema as user_schema
import sqlalchemy.orm as orm
import schemas.post_schema as post_schema


async def create_post(user: user_schema.User, db: orm.Session, post: post_schema.PostCreate):
    post = post_models.Post(**post.dict(), user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_schema.Post.from_orm(post)

async def get_user_posts(user: user_schema.User, db: orm.Session):
    posts = db.query(post_models.Post).filter_by(user_id=user.id)
    return list(map(post_schema.Post.from_orm, posts))

