from fastapi import FastAPI
from datetime import datetime
from .schema import PostGet
from typing import List
import os
import pickle
import pandas as pd
from params import engine


def batch_load_sql(query: str, engine=engine) -> pd.DataFrame:
    CHUNKSIZE = 200000

    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        if "index" in chunk_dataframe.columns:
            chunk_dataframe = chunk_dataframe.drop(columns=["index"])
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


def load_features() -> pd.DataFrame:
    processed_tables = {}

    tables = ["user_data", "post_text_df"]
    for table in tables:
        query = f"SELECT * FROM david_gusejnov_rbh9686_final_project_{table}"

        processed_tables[table] = batch_load_sql(query)

    return processed_tables


def get_model_path(path: str) -> str:
    if (
        os.environ.get("IS_LMS") == "1"
    ):  # проверяем где выполняется код в лмс, или локально. Немного магии
        MODEL_PATH = "/workdir/user_input/model"
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path(
        "/home/dayvi/Рабочий стол/final_project/model/catboost_model.pkl"
    )
    model = pickle.load(open(model_path, "rb"))
    return model


def get_init_dfs(engine=engine):
    df = pd.read_sql(f"SELECT * FROM post_text_df", engine)
    return df


app = FastAPI()
model = load_models()
dfs = load_features()
init_post_df = get_init_dfs()


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
    id: int,
    time: datetime = datetime(year=2021, month=1, day=3, hour=14),
    limit: int = 10,
) -> List[PostGet]:
    user_info = dfs["user_data"][dfs["user_data"]["user_id"] == id]

    df = dfs["post_text_df"].merge(user_info, how="cross")
    predict_df = df.drop(["user_id", "post_id"], axis=1)

    model.predict(predict_df)

    df["score"] = model.predict_proba(predict_df)[:, 1]
    sorted_posts_ids = df.sort_values(by="score", ascending=False)["post_id"].head(
        limit
    )

    top_posts = init_post_df[init_post_df["post_id"].isin(sorted_posts_ids)]

    result = [
        PostGet(id=row["post_id"], text=row["text"], topic=row["topic"])
        for _, row in top_posts.iterrows()
    ]
    return result
