import psycopg
from contextlib import contextmanager
from app.settings import settings

def connect():
    return psycopg.connect(settings.database_url, autocommit=True)

@contextmanager
def get_cursor():
    with connect() as conn:
        with conn.cursor() as cur:
            yield cur
