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
