import sqlite3
import pandas as pd

DB_PATH = "database/processor.db"

def search_data(keyword=None, min_score=None, max_score=None):
    conn = sqlite3.connect(DB_PATH)

    query = "SELECT * FROM texts WHERE 1=1"
    params = []

    if keyword:
        query += " AND text_chunk LIKE ?"
        params.append(f"%{keyword}%")

    if min_score is not None:
        query += " AND sentiment_score >= ?"
        params.append(min_score)

    if max_score is not None:
        query += " AND sentiment_score <= ?"
        params.append(max_score)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    return df