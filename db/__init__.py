import os
import psycopg2
import urllib.parse as urlparse

from flask import g


def get_db():
    conn = psycopg2.connect(
                            database=db_name,
                            user=user_name,
                            password=user_password,
                            host=local,
                            port=psql_post
                            )
    g.db = {'conn': conn, 'cur': conn.cursor()}
    return g.db
