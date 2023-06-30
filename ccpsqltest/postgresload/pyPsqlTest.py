import pandas as pd
import sqlalchemy as sa
import psycopg2
import os
from dotenv import load_dotenv

from time import perf_counter

from querybuilder.playsQueryBuilder import PlayOptions, build_plays_query

load_dotenv()


pg_url = os.getenv("POSTGRESNEON")
sa_engine = sa.create_engine(pg_url)
sa_cursor = sa_engine.connect()


psyconn = psycopg2.connect(
    host="ep-shy-hall-554430.us-west-2.aws.neon.tech",
    port="5432",
    user="sjdefran",
    database="neondb",
    password="dbiu5gvrD3Hs",
)

psy_cursor = psyconn.cursor()


def get_players_plays_against_team(player_id: int, matchup_team_id: int):
    start = perf_counter()
    query = f"""
    select * from plays p1
    join players p2 on p1.pid=p2.pid
    join teams t on t.tid=p1.tid
    join matchups m on
    case 
            when m.htid = t.tid then m.atid={matchup_team_id}
            when m.atid = t.tid then m.htid={matchup_team_id}
    end
    where p1.pid={player_id}
    limit 1000
    """
    print("Making Query")
    plays_result = sa_cursor.execute(query)
    print("Query Returned")
    for play in plays_result:
        print(play)
        break
    end = perf_counter()
    print(end - start)


def get_plays_psy(player_id, matchup_team_id):
    start = perf_counter()
    query = f"""
    select distinct p1.*, p2.fname, p2.lname from plays p1
    left join players p2 on p1.pid=p2.pid
    join teams t on t.tid=p1.tid
    join matchups m on
    case 
            when m.htid = t.tid then m.atid={matchup_team_id}
            when m.atid = t.tid then m.htid={matchup_team_id}
    end
    where p1.pid={player_id} 
    limit 1000; 
    """
    print("Making Query")
    psy_cursor.execute(query)
    print("Query Returned")
    rows = psy_cursor.fetchall()
    for row in rows:
        print(row)
        break
    end = perf_counter()
    print(end - start)


if __name__ == "__main__":
    # get_players_plays_against_team(player_id=1630596, matchup_team_id=1610612755)
    # get_plays_psy(player_id=1630596, matchup_team_id=1610612755)
    opts = PlayOptions(
        player_id=1630209,
        team_id=None,  # if want only when player was on certain team
        matchup_team_id=1610612737,
        limit=1000,
        quarter=4,
    )
