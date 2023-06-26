import pymongo
from pymongo.collection import Collection
from dotenv import load_dotenv
import os

load_dotenv()


def get_db_client_connection() -> pymongo.MongoClient:
    # MONGOPASS = os.getenv("MONGOPASS")
    MONGOURL = os.getenv("MONGOURL")
    client = pymongo.MongoClient(MONGOURL)
    return client


def get_games_collection(client: pymongo.MongoClient) -> Collection:
    db = client["SeasonsV2"]
    collection = db["Games"]
    return collection


def get_playbyplay_collection(client: pymongo.MongoClient) -> Collection:
    db = client["PlayByPlay"]
    collection = db["Games"]
    return collection


def get_teams_dict() -> dict:
    client = get_db_client_connection()
    db = client["TeamsDB"]
    collection = db["Teams"]
    results = collection.find(projection={"_id": False})
    teams = []
    for res in results:
        teams.append(res)
    return teams


def get_all_active_player_ids_on_site() -> set:
    """Scraping all of playbyplay games and creating a set of each player that has had a play"""
    client = get_db_client_connection()
    collection = get_playbyplay_collection(client=client)
    print("Retrieving ALL games")
    results = collection.find(
        projection={"_id": False, "players": True, "game_id": True}
    )
    all_active_ids = set()

    # all_active_ids
    PLAYER_ID_INDEX = 2
    for i, res in enumerate(results):
        # print(f"Starting {i+1} / ~10,700 | {res['game_id']}")
        players_lists = res["players"]
        # print("\tFGM")
        for fgm in players_lists["FGM"]:
            all_active_ids.add(fgm[PLAYER_ID_INDEX])
        # print("\tAST")
        for ast in players_lists["AST"]:
            all_active_ids.add(ast[PLAYER_ID_INDEX])
        # print("\tBLK")
        for blk in players_lists["BLK"]:
            all_active_ids.add(blk[PLAYER_ID_INDEX])
        # print("\tDUNK")
        for dnk in players_lists["DUNK"]:
            all_active_ids.add(dnk[PLAYER_ID_INDEX])
        # print("\tSTL")
        for stl in players_lists["STL"]:
            all_active_ids.add(stl[PLAYER_ID_INDEX])
        # print(f"Finished {i+1} / ~10,700 | {res['game_id']}")

    # write all active ids for testing
    with open("active_ids.txt", "w") as f:
        f.write(all_active_ids.__str__())

    return all_active_ids


def get_matchups_and_matchup_stats_dicts() -> list:
    client = get_db_client_connection()
    collection = get_games_collection(client=client)
    pbp_collection = get_playbyplay_collection(client=client)

    # finding all games in SeasonsV2.Games
    matchups = collection.find(projection={"_id": False})

    # list to keep track of games that are missing playbyplay currently
    # should fix issue w/ broken games
    mismatch_games_list_ids = []

    matchup_data = []
    matchup_stats_data = []
    for i, matchup in enumerate(matchups):
        pbp_game = pbp_collection.find_one({"game_id": matchup["game_id"]})
        # no playbyplay game found, add to list to fix later
        if pbp_game == None:
            mismatch_games_list_ids.append(matchup["game_id"])
            continue  # skip rest of iteration, will add broken games later
        else:
            num_quarters = pbp_game["number_quarters"]
        cur_matchup = {
            "gid": matchup["game_id"],
            "sznstr": matchup["season_str"],
            "date": matchup["date"],
            "htid": matchup["home_info"]["TEAM_ID"],
            "atid": matchup["away_info"]["TEAM_ID"],
            "nquarters": num_quarters,
            "matchupstr": matchup["away_info"]["MATCHUP"],  # BOS @ PHI
            "HWL": matchup["home_info"]["WL"],
            "HFGM": matchup["home_info"]["FGM"],
            "HFGA": matchup["home_info"]["FGA"],
            "HFG_PCT": matchup["home_info"]["FG_PCT"],
            "HFG3M": matchup["home_info"]["FG3M"],
            "HFG3A": matchup["home_info"]["FG3A"],
            "HFG3_PCT": matchup["home_info"]["FG3_PCT"],
            "HFTM": matchup["home_info"]["FTM"],
            "HFTA": matchup["home_info"]["FTA"],
            "HFT_PCT": matchup["home_info"]["FT_PCT"],
            "HOREB": matchup["home_info"]["OREB"],
            "HDREB": matchup["home_info"]["DREB"],
            "HREB": matchup["home_info"]["REB"],
            "HAST": matchup["home_info"]["AST"],
            "HSTL": matchup["home_info"]["STL"],
            "HBLK": matchup["home_info"]["BLK"],
            "HTOV": matchup["home_info"]["TOV"],
            "HPF": matchup["home_info"]["PF"],
            "HPTS": matchup["home_info"]["PTS"],
            "AWL": matchup["away_info"]["WL"],
            "AFGM": matchup["away_info"]["FGM"],
            "AFGA": matchup["away_info"]["FGA"],
            "AFG_PCT": matchup["away_info"]["FG_PCT"],
            "AFG3M": matchup["away_info"]["FG3M"],
            "AFG3A": matchup["away_info"]["FG3A"],
            "AFG3_PCT": matchup["away_info"]["FG3_PCT"],
            "AFTM": matchup["away_info"]["FTM"],
            "AFTA": matchup["away_info"]["FTA"],
            "AFT_PCT": matchup["away_info"]["FT_PCT"],
            "AOREB": matchup["away_info"]["OREB"],
            "ADREB": matchup["away_info"]["DREB"],
            "AREB": matchup["away_info"]["REB"],
            "AAST": matchup["away_info"]["AST"],
            "ASTL": matchup["away_info"]["STL"],
            "ABLK": matchup["away_info"]["BLK"],
            "ATOV": matchup["away_info"]["TOV"],
            "APF": matchup["away_info"]["PF"],
            "APTS": matchup["away_info"]["PTS"],
        }

        # cur_matchup = {
        #     'gid':    matchup['game_id'],
        #     'sznstr': matchup['season_str'],
        #     'date':   matchup['date'],
        #     'htid':   matchup['home_info']['TEAM_ID'],
        #     'atid':   matchup['away_info']['TEAM_ID']
        # }

        # curr_matchup_stats_data = {
        #     'gid':          matchup['game_id'],
        #     'nquarters':    num_quarters,
        #     'matchupstr':   matchup['away_info']['MATCHUP'], # BOS @ PHI
        #     'HWL':          matchup['home_info']['WL'],
        #     'HFGM':         matchup['home_info']['FGM'],
        #     'HFGA':         matchup['home_info']['FGA'],
        #     'HFG_PCT':      matchup['home_info']['FG_PCT'],
        #     'HFG3M':        matchup['home_info']['FG3M'],
        #     'HFG3A':        matchup['home_info']['FG3A'],
        #     'HFG3_PCT':     matchup['home_info']['FG3_PCT'],
        #     'HFTM':         matchup['home_info']['FTM'],
        #     'HFTA':         matchup['home_info']['FTA'],
        #     'HFT_PCT':      matchup['home_info']['FT_PCT'],
        #     'HOREB':        matchup['home_info']['OREB'],
        #     'HDREB':        matchup['home_info']['DREB'],
        #     'HREB':         matchup['home_info']['REB'],
        #     'HAST':         matchup['home_info']['AST'],
        #     'HSTL':         matchup['home_info']['STL'],
        #     'HBLK':         matchup['home_info']['BLK'],
        #     'HTOV':         matchup['home_info']['TOV'],
        #     'HPF':          matchup['home_info']['PF'],
        #     'HPTS':         matchup['home_info']['PTS'],
        #     'AWL':          matchup['away_info']['WL'],
        #     'AFGM':         matchup['away_info']['FGM'],
        #     'AFGA':         matchup['away_info']['FGA'],
        #     'AFG_PCT':      matchup['away_info']['FG_PCT'],
        #     'AFG3M':        matchup['away_info']['FG3M'],
        #     'AFG3A':        matchup['away_info']['FG3A'],
        #     'AFG3_PCT':     matchup['away_info']['FG3_PCT'],
        #     'AFTM':         matchup['away_info']['FTM'],
        #     'AFTA':         matchup['away_info']['FTA'],
        #     'AFT_PCT':      matchup['away_info']['FT_PCT'],
        #     'AOREB':        matchup['away_info']['OREB'],
        #     'ADREB':        matchup['away_info']['DREB'],
        #     'AREB':         matchup['away_info']['REB'],
        #     'AAST':         matchup['away_info']['AST'],
        #     'ASTL':         matchup['away_info']['STL'],
        #     'ABLK':         matchup['away_info']['BLK'],
        #     'ATOV':         matchup['away_info']['TOV'],
        #     'APF':          matchup['away_info']['PF'],
        #     'APTS':         matchup['away_info']['PTS'],
        # }

        # Add dict to overall list to be converted to df later
        matchup_data.append(cur_matchup)
        # matchup_stats_data.append(curr_matchup_stats_data)
        print(
            f"Finished | {matchup['away_info']['MATCHUP']} | {matchup['date']} | {i+1} / 11498"
        )

    # write out broken game ids for later
    with open("brokenGames.txt", "w") as f:
        f.write(mismatch_games_list_ids.__str__())
    # return (matchup_data, matchup_stats_data)
    return matchup_data


def create_plays_list():
    client = get_db_client_connection()
    pbp_collection = get_playbyplay_collection(client=client)
    play_types = ["FGM", "AST", "STL", "BLK", "DUNK"]

    final_plays_list = []
    i = 0
    for i, game in enumerate(pbp_collection.find(projection={"_id": False})):
        plays_dict = game["plays"]
        game_id = game["game_id"]

        # iterate through each play type array
        for pt in play_types:
            plays = plays_dict[pt]  # game['plays']['FGM']
            # plays in playtype array
            for play in plays:
                transformed_play = {
                    "pid": play["playerID"],
                    "gid": game_id,
                    "description": play["description"],
                    "type": pt,  # 'FGM' etc
                    "url": play["url"],
                    "tid": play["teamID"],
                    "hscore": play["scoreHome"],
                    "ascore": play["scoreAway"],
                    "time": play["time"],
                }
                final_plays_list.append(transformed_play)

        print(f"Finished | {game_id} | {i+1}/~10,718")
    return final_plays_list
