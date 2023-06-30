import pandas as pd

from table_schemas import SCHEMAS, PANDAS_SCHEMA

df1 = pd.read_csv("csvdata//MatchupsV4.csv", dtype=PANDAS_SCHEMA["matchups"])

df2 = pd.read_csv("csvdata//MatchupsV3.csv", dtype=PANDAS_SCHEMA["matchups"])


select_cols = ["gid", "htid", "atid"]

joined_df = df1.merge(df2[select_cols], on="gid", how="left")

print(joined_df)


# df.rename(columns={"type": "ptype", "time": "ptime"}, inplace=True)


# print(df)
joined_df.to_csv("csvdata/MatchupsV5.csv", index=False)
