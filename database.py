import sqlite3
import pandas as pd

DB_NAME = "database/career_platform.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()

    # Database me students table hai ya nahi check karo
    table_exists = pd.read_sql(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='students'
        """,
        conn
    )

    # Sirf pehli baar CSV se data import hoga
    if table_exists.empty:

        df = pd.read_csv("student.csv")

        df.to_sql(
            "students",
            conn,
            if_exists="fail",
            index=False
        )

        print("Database created from student.csv")

    else:
        print("Database already exists")

    conn.close()