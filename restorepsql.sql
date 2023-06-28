-- Restore script

-- Indexes ---------------------------------

  --plays
DROP INDEX IF EXISTS plays_gid_idx;
DROP INDEX IF EXISTS plays_pid_idx;

CREATE INDEX plays_gid_idx ON plays(gid);
CREATE INDEX plays_pid_idx ON plays(pid);

  --teams
DROP INDEX IF EXISTS teams_tid;
CREATE INDEX teams_tid on teams(tid);

  --players
DROP INDEX IF EXISTS players_pid;
DROP INDEX IF EXISTS players_tid;
CREATE INDEX players_pid on players(pid);
CREATE INDEX players_tid on players(tid);

  --matchups
DROP INDEX IF EXISTS matchups_gid;
CREATE INDEX matchups_gid on matchups(gid);
-------------------------------------------------------------

-- Primary Keys
----------------------------------------------
ALTER TABLE plays DROP CONSTRAINT IF EXISTS pk_plays;
ALTER TABLE matchups DROP CONSTRAINT IF EXISTS pk_matchups;
ALTER TABLE players DROP CONSTRAINT IF EXISTS pk_players;
ALTER TABLE teams DROP CONSTRAINT IF EXISTS pk_teams;

ALTER TABLE plays ADD CONSTRAINT pk_plays PRIMARY KEY (playid);
ALTER TABLE players ADD CONSTRAINT pk_players PRIMARY KEY (pid);
ALTER TABLE teams ADD CONSTRAINT pk_teams PRIMARY KEY (tid);
ALTER TABLE matchups ADD CONSTRAINT pk_matchups PRIMARY KEY (gid);
-----------------------------------------------------------
