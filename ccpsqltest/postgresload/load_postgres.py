"""
Creates dataframes from csvdata/ using SCHEMAS & PANDAS_SCHEMA

Then inserts tables into postgres
"""

import sqlite3
import pandas as pd

import sqlalchemy as sa
import psycopg
import os
from dotenv import load_dotenv

from table_schemas import SCHEMAS, PANDAS_SCHEMA

load_dotenv()
TABLES_TO_CSV_FILE_NAMES = {
    "matchups": "MatchupsV5.csv",
    # "players": "Players.csv",
    # "teams": "Teams.csv",
    # "plays": "PlaysV3.csv",
}
CSV_DIR_NAME = "csvdata"
# connection = sqlite3.connect('test.db')

# pg_url = os.getenv("POSTGRESURL")
# conn_dict = psycopg.conninfo.conninfo_to_dict(pg_url)
# connection = psycopg.connect(**conn_dict)

# sqliteConnection = sqlite3.connect("test.db")

# sa_lite_engine = sa.create_engine("sqlite:///school.db")

pg_url = os.getenv("POSTGRESNEON")
sa_connection = sa.create_engine(pg_url)


def create_tables():
    import os

    for table in TABLES_TO_CSV_FILE_NAMES.keys():
        print(f"Starting {table}")
        path = os.path.join(CSV_DIR_NAME, TABLES_TO_CSV_FILE_NAMES[table])
        temp_df = pd.read_csv(path, dtype=PANDAS_SCHEMA[table])
        temp_df.to_sql(
            name=table,
            con=sa_connection,
            index=False,
            if_exists="replace",
            dtype=SCHEMAS[table],
        )


# def psql_query_test():
#     cursor = connection.cursor()
#     test = cursor.execute("SELECT * FROM players;")
#     print(test)
def test_plays_query():
    sac = sa_connection.connect()
    cursor_result = sac.execute("Select * from players")
    test_list = []
    for result in cursor_result:
        test_list.append(result)

    df = pd.DataFrame(data=test_list, dtype=PANDAS_SCHEMA["players"])
    print(df)


if __name__ == "__main__":
    create_tables()
    # test_plays_query()
    # psql_query_test()
