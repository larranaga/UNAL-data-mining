import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

user_mean = {}
critic_mean = {}
count = {}


def get_mean(count, developer, user):
    if user:
        return count[developer]["user_score"] / count[developer]["user_count"] if count[developer]["user_count"] > 0 else 0
    else:
        return count[developer]["critic_score"] / count[developer]["critic_count"] if count[developer]["critic_count"] > 0 else 0


def new_critic_score(entry):
    if entry["Critic_Score"] == 0:
        return critic_mean[entry["Developer"]]
    return entry["Critic_Score"]


def new_user_score(entry):
    if entry["User_Score"] == 0:
        return user_mean[entry["Developer"]]
    return entry["User_Score"]

def remove_zero_from_user(entry):
    if entry["User_Score"] == 0:
        return np.NaN
    return entry["User_Score"]

def remove_zero_from_critic(entry):
    if entry["Critic_Score"] == 0:
        return np.NaN
    return entry["Critic_Score"]


videogames_data = pd.read_csv("processed_videogames_data_3.csv")
videogames_data.drop('Number_of_Records', 1, inplace=True)
videogames_data["NA_Sales"] = videogames_data.apply(lambda entry : entry["NA_Sales"].replace("K", "000"), axis=1)
videogames_data["NA_Sales"] = videogames_data["NA_Sales"].astype(int)

videogames_data["EU_Sales"] = videogames_data.apply(lambda entry : entry["EU_Sales"].replace("K", "000"), axis=1)
videogames_data["EU_Sales"] = videogames_data["EU_Sales"].astype(int)

videogames_data["JP_Sales"] = videogames_data.apply(lambda entry : entry["JP_Sales"].replace("K", "000"), axis=1)
videogames_data["JP_Sales"] = videogames_data["JP_Sales"].astype(int)

videogames_data["Other_Sales"] = videogames_data.apply(lambda entry : entry["Other_Sales"].replace("K", "000"), axis=1)
videogames_data["Other_Sales"] = videogames_data["Other_Sales"].astype(int)

videogames_data["Global_Sales"] = videogames_data["NA_Sales"] + videogames_data["EU_Sales"] \
                                + videogames_data["JP_Sales"] + videogames_data["Other_Sales"]


developers = videogames_data["Developer"].unique()

for developer in developers:
    count[developer] = {
        "user_score" : 0.0,
        "user_count": 0,
        "critic_score": 0.0,
        "critic_count": 0
    }


for index, entry in videogames_data.iterrows():
    if entry["User_Score"] != 0.0:
        count[entry["Developer"]]["user_score"] += entry["User_Score"]
        count[entry["Developer"]]["user_count"] += 1
    if entry["Critic_Score"] != 0.0 :
        count[entry["Developer"]]["critic_score"] += entry["Critic_Score"]
        count[entry["Developer"]]["critic_count"] += 1

for developer in developers:
    user_mean[developer] = get_mean(count, developer, user=True)
    critic_mean[developer] = get_mean(count, developer, user=False)


videogames_data["Critic_Score"] = videogames_data.apply(new_critic_score, axis=1)
videogames_data["User_Score"] = videogames_data.apply(new_user_score, axis=1)


videogames_data.drop(videogames_data[(videogames_data.Critic_Score == 0)
                                     & (videogames_data.User_Score == 0)].index, inplace=True)

videogames_data["Critic_Score"] = videogames_data.apply(remove_zero_from_critic, axis=1)
videogames_data["User_Score"] = videogames_data.apply(remove_zero_from_user, axis=1)

videogames_data["Critic_Score"].fillna(videogames_data["User_Score"],inplace=True)
videogames_data["User_Score"].fillna(videogames_data["Critic_Score"],inplace=True)

print(videogames_data.describe())

videogames_data["Rating"] = pd.factorize(videogames_data["Rating"])[0]
videogames_data["Developer"] = pd.factorize(videogames_data["Developer"])[0]
videogames_data["Publisher"] = pd.factorize(videogames_data["Publisher"])[0]
videogames_data["Genre"] = pd.factorize(videogames_data["Genre"])[0]

names = videogames_data["Name"]
videogames_data.drop("Name",1, inplace=True )
pca = PCA(n_components=4)

pca_info = pca.fit(videogames_data)

print(pca_info.components_)
print()

for explanation in pca_info.explained_variance_ratio_.cumsum():
    print(explanation)

videogames_data = pca.fit(videogames_data).transform(videogames_data)

csv_data = pd.DataFrame(videogames_data)
csv_data.to_csv("complete_processed_videogames_data.csv", index=False, header=False)