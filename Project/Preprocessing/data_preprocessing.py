import pandas as pd
import numpy as np

mode = {}

def process_info(info):
    d = {}
    d["Name"] = info.iloc[0]["Name"]

    d["Platform"] = info.iloc[0]["Platform"]
    d["Year_of_Release"] = info.iloc[0]["Year_of_Release"]
    d["Genre"] = info.iloc[0]["Genre"]
    d["Publisher"] = info.iloc[0]["Publisher"]
    d["Developer"] = info.iloc[0]["Developer"]
    d["Rating"] = info.iloc[0]["Rating"]
    d["NA_Sales"] = info["NA_Sales"].sum()
    d["EU_Sales"] = info["EU_Sales"].sum()
    d["JP_Sales"] = info["JP_Sales"].sum()
    d["Other_Sales"] = info["Other_Sales"].sum()
    d["Global_Sales"] = info["Global_Sales"].sum()
    d["Critic_Score"] = info["Critic_Score"].sum()
    d["Critic_Count"] = info["Critic_Count"].sum()
    d["User_Score"] = info["User_Score"].sum()
    d["User_Count"] = info["User_Count"].sum()

    if d["User_Score"] > 0:
        d["User_Score"] /= info["User_Score"][info["User_Score"] > 0].count()
    if d["Critic_Score"] > 0:
        d["Critic_Score"] /= info["Critic_Score"][info["Critic_Score"] > 0].count()

    ans = pd.DataFrame([d])
    return ans


def get_mode(count, developer, ratings):
    best = 0
    ans = ""
    for rating in ratings:
        if not pd.isna(rating) and count[developer][rating] >= best:
            best = count[developer][rating]
            ans = rating
    return ans

def new_rating(entry):
    if(pd.isna(entry["Rating"])):
        return mode[entry["Developer"]]
    return entry["Rating"]


videogames_data = pd.read_csv("Video_Games_Sales_as_at_22_Dec_2016.csv")
videogames_data.dropna(subset=["Name"], inplace=True)

videogames_data.drop(videogames_data[(pd.isna(videogames_data.Publisher))
                                     & (pd.isna(videogames_data.Developer))].index, inplace=True)

videogames_data.drop(videogames_data[videogames_data["User_Score"] == "tbd"].index, inplace=True)
videogames_data["User_Score"] = videogames_data["User_Score"].astype(float)

videogames_data.drop(videogames_data[videogames_data["User_Score"] > 10].index, inplace=True)
videogames_data.drop(videogames_data[videogames_data["Critic_Score"] > 100].index, inplace=True)

videogames_data["Publisher"].fillna(videogames_data["Developer"], inplace=True)
videogames_data["Developer"].fillna(videogames_data["Publisher"], inplace=True)
videogames_data["Year_of_Release"] =\
    videogames_data["Year_of_Release"].fillna(videogames_data["Year_of_Release"].mean())

developers = videogames_data["Developer"].unique()
ratings = videogames_data["Rating"].unique()

count = {}
for developer in developers:
    count[developer] = {}
    for rating in ratings:
        if not pd.isna(rating):
            count[developer][rating] = 0

for index, entry in videogames_data.iterrows():
    if (not pd.isna(entry["Rating"])):
        count[entry["Developer"]][entry["Rating"]] += 1


for developer in developers:
    mode[developer] = get_mode(count, developer, ratings)


videogames_data["Rating"] = videogames_data.apply(new_rating, axis=1)

videogames_data["Critic_Score"].fillna(0, inplace=True)
videogames_data["Critic_Count"].fillna(0, inplace=True)
videogames_data["User_Score"].fillna(0, inplace=True)
videogames_data["User_Count"].fillna(0, inplace=True)

videogames_data["Critic_Score"] = videogames_data["Critic_Score"]/10

names = videogames_data.Name.unique()

for name in names:
    info = videogames_data.loc[videogames_data["Name"] == name]
    new_data = process_info(info)
    videogames_data.drop(videogames_data[videogames_data["Name"] == name].index, inplace=True)
    videogames_data = videogames_data.append(new_data)

videogames_data.to_csv("processed_videogames_data.csv")