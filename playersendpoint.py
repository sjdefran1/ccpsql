import requests

from json import dumps

req_headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


def get_player_common_info(player_id: int):
    try:
        url = f"https://stats.nba.com/stats/commonplayerinfo?LeagueID=&PlayerID={player_id}"
        response = requests.get(url=url, headers=req_headers)
        result = response.json()

        attrs_labels = result["resultSets"][0]["headers"]
        attrs_values = result["resultSets"][0]["rowSet"][0]
        stats_values = result["resultSets"][1]["rowSet"][0]

        attr_remaps = {
            "PERSON_ID": "pid",
            "FIRST_NAME": "fname",
            "LAST_NAME": "lname",
            "DISPLAY_FI_LAST": "nameabbr",
            "SEASON_EXP": "yrsplayed",
            "JERSEY": "jerseynum",
            "POSITION": "pos",
            "ROSTERSTATUS": "status",
            "TEAM_ID": "tid",
            "GREATEST_75_FLAG": "goatflag",
            "COUNTRY": "country",
            "HEIGHT": "height",
            "WEIGHT": "weight",
        }
        ret_dict = {}
        # Common attributes (name, id, jersey etc)
        for i, header in enumerate(attrs_labels):
            try:
                remap_val = attr_remaps[header]
                ret_dict[remap_val] = attrs_values[i]
            except:  # header not included in remap, move on
                pass

        # Stats
        stats_dict = {
            "statstr": stats_values[2],
            "PTS": stats_values[3],
            "AST": stats_values[4],
            "REB": stats_values[5],
        }
        # sorry future me, auto formatter horrible choice
        ret_dict[
            "avatarurl"
        ] = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"

        ret_dict = {**ret_dict, **stats_dict}

        return ret_dict
    except Exception as e:
        print(e)
        print(f"{player_id} Failed")
        return None


if __name__ == "__main__":
    d = get_player_common_info(1717)
    print(d)
    # print("boopit ")
