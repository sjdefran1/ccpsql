import pandas as pd

from table_schemas import SCHEMAS, PANDAS_SCHEMA

df = pd.read_csv("csvdata//MatchupsV2.csv", dtype=PANDAS_SCHEMA["matchups"])


drop_cols = [
    "HWL",
    "HFGM",
    "HFGA",
    "HFG_PCT",
    "HFG3M",
    "HFG3A",
    "HFG3_PCT",
    "HFTM",
    "HFTA",
    "HFT_PCT",
    "HOREB",
    "HDREB",
    "HREB",
    "HAST",
    "HSTL",
    "HBLK",
    "HTOV",
    "HPF",
    "AWL",
    "AFGM",
    "AFGA",
    "AFG_PCT",
    "AFG3M",
    "AFG3A",
    "AFG3_PCT",
    "AFTM",
    "AFTA",
    "AFT_PCT",
    "AOREB",
    "ADREB",
    "AREB",
    "AAST",
    "ASTL",
    "ABLK",
    "ATOV",
    "APF",
]

df = df.drop(drop_cols, axis=1)
df.to_csv("csvdata/MatchupsV3.csv", index=False)
