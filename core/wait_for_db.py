import time
import pymysql
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:72942250@172.31.16.52:8005/bd_usuarios"

def wait_for_db():
    while True:
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            break
        except Exception as e:
            print("Database is not ready yet. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()