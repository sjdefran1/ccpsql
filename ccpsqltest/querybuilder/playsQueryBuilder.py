from pydantic import BaseModel
from querybuilder.playSql import *  # sql queries
from ccpsqltest.RequestModels import PlayOptions


def build_plays_query(opts: PlayOptions) -> str:
    """
    Builds sql query string for given options
    """
    ret_query = BASE_QUERY
    delimiter = ""
    # Games vs other teams || specific game
    # cant be both
    if opts.matchup_team_id:
        add_str = MATHCUPS_OPT.format(opts.matchup_team_id, opts.matchup_team_id)
        ret_query = delimiter.join([ret_query, add_str])
    elif opts.gid:
        add_str = GID_OPTS.format(opts.gid)
        ret_query = delimiter.join([ret_query, add_str])

    # only plays from when player was on specific team
    if opts.team_id:
        add_str = TEAMID_OPTS.format(opts.team_id)
        ret_query = delimiter.join([ret_query, add_str])

    # only by quarter
    if opts.quarter:
        add_str = QUARTER_OPT.format(opts.quarter)
        ret_query = delimiter.join([ret_query, add_str])

    # only fgm etc
    if opts.stat_type:
        add_str = STAT_TYPE_OPTS.format(opts.stat_type)
        ret_query = delimiter.join([ret_query, add_str])

    # where pid=player_id && limit
    ret_query = delimiter.join([ret_query, BASE_OPTS.format(opts.player_id)])
    ret_query = delimiter.join([ret_query, LIMIT_OPTS.format(opts.limit)])
    return ret_query


if __name__ == "__main__":
    opts_var = PlayOptions(
        player_id=1630209,
        team_id=None,  # if want only when player was on certain team
        matchup_team_id=1610612737,
        limit=1000,
        quarter=4,
    )

    # print(opts_var.__str__())
    # print(build_plays_query(opt=opts_var))
