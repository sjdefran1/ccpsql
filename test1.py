import pandas as pd

data = [{"pid": 1630208, "fname": "Nick", "lname": "Richards", "bday": "1997-11-29T00:00:00", "school": "Kentucky", "height": "7-0", "weight": "245", "yrsplayed": 3, "jerseynum": "4", "pos": "Center", "status": "Active", "tid": 1610612766, "tname": "Hornets", "tcity": "Charlotte", "firstyr": 2020, "goatflag": "N"}, {"pid": 1630209, "fname": "Omer", "lname": "Yurtseven", "bday": "1998-06-19T00:00:00", "school": "Georgetown", "height": "6-11", "weight": "275", "yrsplayed": 2, "jerseynum": "77", "pos": "Center", "status": "Active", "tid": 1610612748, "tname": "Heat", "tcity": "Miami", "firstyr": 2020, "goatflag": "N"}]

df = pd.DataFrame(data=data)
# df.set_index('pid', inplace=True)

print(df)

# df2 = pd.read_csv("csvtest.csv")

# print(df2)

