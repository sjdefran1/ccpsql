BASE_QUERY = """
select distinct 
    p1.*, 
    p2.fname, 
    p2.lname 
from plays p1
left join players p2 on 
    p1.pid=p2.pid
join teams t on 
    t.tid=p1.tid
"""

MATHCUPS_OPT = """
join matchups m on
    case 
        when m.htid = t.tid then m.atid={}
        when m.atid = t.tid then m.htid={}
    end
"""

QUARTER_OPT = """
and p1.quarter={}
"""

STAT_TYPE_OPTS = """
and p1.ptype='{}'
"""

GID_OPTS = """
and p1.gid={}
"""

TEAMID_OPTS = """
and p1.tid={}
"""

BASE_OPTS = """
where p1.pid={}
"""

LIMIT_OPTS = """
limit {}
"""

# POSSIBLE SCENARS

"""
------------------------------------------
- All plays from player
    ops:
        (stat-type)
        (quarter)

- All plays from player in season 
    ops: 
        (stat-type) 
        (quarter)

- All plays from player in game 
    opts: 
        (gid) 
        (stat-type) 
        (quarter) 

-----------------------------------------
- All play from player vs matchup 
    opts: 
        (mtid)
        (stat-type) 
        (quarter)

BASE_QUERY = 
select distinct p1.*, p2.fname, p2.lname from plays p1
left join players p2 on p1.pid=p2.pid
join teams t on t.tid=p1.tid

MATCHUPS =
join matchups m on
  case 
        when m.htid = t.tid then m.atid={}
        when m.atid = t.tid then m.htid={}
  end

OPTS_BASE =
where p1.pid={}

OPTS_QUARTER=
AND p1.quarter={}

OPTS_LIMIT=
limit 1000

OPTS_STAT_TYPE=
AND p1.ptype={}

OPTS_SINGLE_GAME=
AND p1.gid={}


"""
