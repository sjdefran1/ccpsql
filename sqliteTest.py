import sqlite3
import pandas as pd

import sqlalchemy as sa
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
TABLES_TO_CSV_FILE_NAMES = {
    "plays": "Plays.csv",
}
CSV_DIR_NAME = "csvdata"
# connection = sqlite3.connect('test.db')

pg_url = os.getenv("POSTGRESURL")
conn_dict = psycopg.conninfo.conninfo_to_dict(pg_url)
connection = psycopg.connect(**conn_dict)
sa_connection = sa.create_engine(pg_url)
# sqliteConnection = sqlite3.connect("test.db")


def create_tables():
    import os

    for table in TABLES_TO_CSV_FILE_NAMES.keys():
        print(f"Starting {table}")
        path = os.path.join(CSV_DIR_NAME, TABLES_TO_CSV_FILE_NAMES[table])
        temp_df = pd.read_csv(path)
        temp_df.to_sql(name=table, con=sa_connection, index=False, if_exists="replace")


# def psql_query_test():
#     cursor = connection.cursor()
#     test = cursor.execute("SELECT * FROM players;")
#     print(test)


if __name__ == "__main__":
    create_tables()
    # psql_query_test()
