from databaseutil import (
    get_all_active_player_ids_on_site,
    get_matchups_and_matchup_stats_dicts,
    get_teams_dict,
    create_plays_list,
)
from playersendpoint import get_player_common_info
from time import sleep
import pandas as pd
import os

from activeIDS import IDS

CSV_FILE_NAMES = {
    "players": "Players.csv",
    "matchups": "MatchupsV4.csv",
    "matchup_stats": "MatchupStats.csv",
    "teams": "Teams.csv",
    "plays": "PlaysV3.csv",
}
CSV_DIR_NAME = "csvdata"


def create_players_dataframe():
    """Creates dict for every player that has a play on the site"""
    # all_ids = get_all_active_player_ids_on_site()
    all_ids = IDS
    all_players = []
    for i, id in enumerate(all_ids):
        player = get_player_common_info(id)
        if player == None:
            continue
        all_players.append(player)
        print(f"Recived {player['fname']} {player['lname']} {i+1}/{len(all_ids)}")
        sleep(0.5)

    # create csv for testing
    df = pd.DataFrame(data=all_players)
    df.set_index("pid", inplace=True)
    df.to_csv(os.path.join(CSV_DIR_NAME, CSV_FILE_NAMES["players"]))


def create_matchup_and_stats_dataframes():
    matchups_and_stats = get_matchups_and_matchup_stats_dicts()
    matchups_df = pd.DataFrame(matchups_and_stats[0])
    matchups_df.set_index("gid", inplace=True)
    matchups_df.to_csv("matchups.csv")
    matchups_stats_df = pd.DataFrame(matchups_and_stats[1])
    matchups_stats_df.to_csv(
        os.path.join(CSV_DIR_NAME, CSV_FILE_NAMES["matchup_stats"]),
        index=True,
        index_label="msid",
    )


def create_matchupV2():
    matchups_and_stats = get_matchups_and_matchup_stats_dicts()
    matchups_df = pd.DataFrame(data=matchups_and_stats)
    matchups_df.set_index("gid", inplace=True)
    matchups_df.to_csv(os.path.join(CSV_DIR_NAME, CSV_FILE_NAMES["matchups"]))


def create_teams_dataframe():
    teams = get_teams_dict()
    teams_df = pd.DataFrame(data=teams)
    teams_df = teams_df.rename(columns={"id": "tid"})
    teams_df.set_index("tid", inplace=True)
    teams_df.to_csv(os.path.join(CSV_DIR_NAME, CSV_FILE_NAMES["teams"]))


def create_plays_dataframe():
    plays = create_plays_list()
    plays_df = pd.DataFrame(data=plays)
    plays_df.to_csv(
        os.path.join(CSV_DIR_NAME, CSV_FILE_NAMES["plays"]),
        index=True,
        index_label="playid",
    )


if __name__ == "__main__":
    # create_players_dataframe()
    # create_matchup_and_stats_dataframes()
    # create_matchupV2()
    # create_teams_dataframe()
    create_plays_dataframe()
    # d = parse_all_players_txt()
    # print(d)
