from fastapi import FastAPI, Depends, HTTPException
from .schema import UserGet, PostGet, FeedGet
from .tables.table_post import Post
from .tables.table_user import User
from .tables.table_feed import Feed
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from features_load import load_features
from model_path import load_models
from .database import SessionLocal


app = FastAPI()
model = load_models()
dfs = load_features()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    res = db.query(User).filter(User.id == id).one_or_none()
    if not res:
        raise HTTPException(404, ":(")
    return res


@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    res = db.query(Post).filter(Post.id == id).one_or_none()
    if not res:
        raise HTTPException(404, ":(")
    return res


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_feed(id: int, db: Session = Depends(get_db), limit=10):
    return (
        db.query(Feed)
        .filter(Feed.user_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_feed(id: int, db: Session = Depends(get_db), limit=10):
    return (
        db.query(Feed)
        .filter(Feed.post_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_reco(db: Session = Depends(get_db), id=None, limit=10):
    result = (
        db.query(Post)
        .join(Feed)
        .filter(Feed.action == "like")
        .group_by(Post.id)
        .order_by(func.count(Post.id).desc())
        .limit(limit)
        .all()
    )
    return result


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(id: int, time: datetime, limit: int = 10) -> List[PostGet]:
    user_info = dfs["user_data"][dfs["user_data"]["user_id"] == id]

    df = dfs["post_text_df"].merge(user_info, how="cross")
    predict_df = df.drop(["user_id", "post_id"], axis=1)

    model.predict(predict_df)

    df["score"] = model.predict_proba(predict_df)[:, 1]
    top_posts = df.sort_values(by="score", ascending=False)["score"].head(limit)

    return top_posts
