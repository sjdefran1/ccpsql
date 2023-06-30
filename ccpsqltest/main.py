import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import sqlalchemy as sa
import pandas as pd
from dotenv import load_dotenv
from time import perf_counter


from querybuilder.playsQueryBuilder import build_plays_query
from postgresload.table_schemas import *
from RequestModels import PlayOptions

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("\tCONNECTING TO DATABASE")
    global psy_cursor
    # sa_engine = sa.create_engine(PG_URL)
    psyconn = psycopg2.connect(
        host="ep-shy-hall-554430.us-west-2.aws.neon.tech",
        port="5432",
        user="sjdefran",
        database="neondb",
        password="dbiu5gvrD3Hs",
    )
    psy_cursor = psyconn.cursor()
    print("\tFINISHED")


@app.get("/teams")
async def get_all_teams_controller():
    """
    Returns teams table from mongodb
    Common information for each team, name, city, teamid
    """
    psy_cursor.execute("SELECT * FROM teams")
    ret_list = []
    for res in psy_cursor.fetchall():
        ret_list.append(res)

    return JSONResponse(content=ret_list)


@app.get("/query")
async def query_builder_test(opts: PlayOptions):
    query = build_plays_query(opts=opts)
    psy_cursor.execute(query)
    print("Query Returned")
    rows = psy_cursor.fetchall()
    return JSONResponse(content=rows, status_code=200)


@app.on_event("shutdown")
async def shutdown():
    print("\tCLOSING CURSOR")
    # sa_cursor.close()
    psy_cursor.close()
    print("\tCLOSED")


if __name__ == "__main__":
    import uvicorn

    load_dotenv()
    PG_URL = os.getenv("POSTGRESNEON")
    uvicorn.run(app, host="localhost", port=8000)


"""

USE VIEWS FOR SOMETHING LIKE all plays from player

Allows for pagination if i added an incrementing column to view??

gets rid of problem playids will be spread out making it so cant use
offset

"""


# @app.get("/plays2")
# def get_plays_sa(options: PlayOptions):
#     start = perf_counter()
#     query = f"""
#     select * from plays p1
#     join players p2 on p1.pid=p2.pid
#     join teams t on t.tid=p1.tid
#     join matchups m on
#     case
#             when m.htid = t.tid then m.atid={options.matchup_team_id}
#             when m.atid = t.tid then m.htid={options.matchup_team_id}
#     end
#     where p1.pid={options.player_id}
#     limit 1000
#     """
#     print("Making Query")
#     plays_result = sa_cursor.execute(query)
#     # df = pd.DataFrame(
#     #     data=plays_result.all(), columns=[key for key in plays_result.keys()]
#     # )
#     cols = [key for key in plays_result.keys()]
#     print(cols)
#     print("Query Returned")
#     # print(df)
#     # for play in plays_result:
#     #     print(play)
#     #     break
#     end = perf_counter()
#     print(end - start)
#     return plays_result
