import pandas as pd
from db import get_db


def executeQuery(query, fetch):
    db = get_db()
    conn = db["conn"]
    cur = db["cur"]
    cur.execute(query)
    res = []
    if fetch == 'one':
        res = cur.fetchone()
    elif fetch == 'all':
        res = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return res


def getDF(tablename):
    db = get_db()
    conn = db["conn"]
    df = pd.read_sql_query(f"select * from {tablename};", con=conn)
    conn.close()
    return df
