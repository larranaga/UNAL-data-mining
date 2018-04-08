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


def categorize_critic_score(entry):
    score = entry["Critic_Score"]
    if score > 8.5:
        return "High"
    elif score > 6:
        return "Medium"
    elif score > 4:
        return "Low"
    else:
        return "Worst"


def categorize_user_score(entry):
    score = entry["User_Score"]
    if score > 8.5:
        return "High"
    elif score > 6:
        return "Medium"
    elif score > 4:
        return "Low"
    else:
        return "Worst"


def categorize_na_sales(entry):
    sales = entry["NA_Sales"]
    top = 10000000
    if sales > top:
        return "Top"
    category = 0
    delta = 500000
    low = 500000
    for i in range(low, top + 1, delta):
        if(sales >= i - delta and sales <= i):
            return str(category)
        category+=1
    return "error"


def categorize_jp_sales(entry):
    sales = entry["JP_Sales"]
    top = 5000000
    if sales > top:
        return "Top"
    category = 0
    delta = 500000
    low = 500000
    for i in range(low, top + 1, delta):
        if sales >= i - delta and sales <= i:
            return str(category) + "c"
        category += 1
    return "error"


def categorize_eu_sales(entry):
    sales = entry["EU_Sales"]
    top = 10000000
    if sales > top:
        return "Top"
    category = 0
    delta = 500000
    low = 500000
    for i in range(low, top + 1, delta):
        if (sales >= i - delta and sales <= i):
            return str(category)
        category += 1
    return "error"


def categorize_other_sales(entry):
    sales = entry["Other_Sales"]
    top = 2500000
    if sales > top:
        return "Top"
    category = 0
    delta = 500000
    low = 500000
    for i in range(low, top + 1, delta):
        if sales >= i - delta and sales <= i:
            return str(category)
        category += 1
    return "error"


def categorize_global_sales(entry):
    sales = entry["Global_Sales"]
    top = 15000000
    if sales > top:
        return "Top"
    category = 0
    delta = 50000
    low = 50000
    for i in range(low, top + 1, delta):
        if (sales >= i - delta and sales <= i):
            return str(category)
        category += 1
    print("error")
    print(entry.Name)
    print(sales)
    print(sales + 1)
    return "error"

videogames_data = pd.read_csv("processed_videogames_data.csv")
#videogames_data.drop('Number_of_Records', 1, inplace=True)

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

#print(videogames_data.describe())

#videogames_data["Rating"] = pd.factorize(videogames_data["Rating"])[0]

videogames_data["Nominal_Critic_Score"] = videogames_data.apply(categorize_critic_score, axis=1)
videogames_data["Nominal_User_Score"] = videogames_data.apply(categorize_user_score, axis=1)
videogames_data["Nominal_NA_Sales"] = videogames_data.apply(categorize_na_sales, axis=1)
videogames_data["Nominal_JP_Sales"] = videogames_data.apply(categorize_jp_sales, axis=1)
videogames_data["Nominal_EU_Sales"] = videogames_data.apply(categorize_eu_sales, axis=1)
videogames_data["Nominal_Other_Sales"] = videogames_data.apply(categorize_other_sales, axis=1)
videogames_data["Nominal_Global_Sales"] = videogames_data.apply(categorize_global_sales, axis=1)

videogames_data.to_csv("complete_processed_nominal_videogames_data.csv", index=False, header=True)


target = pd.DataFrame()
target["Name"] = videogames_data["Name"]
target["NA_Sales"] = videogames_data["NA_Sales"]
target["JP_Sales"] = videogames_data["JP_Sales"]
target["EU_Sales"] = videogames_data["EU_Sales"]
target["Other_Sales"] = videogames_data["Other_Sales"]
target["Global_Sales"] = videogames_data["Global_Sales"]

videogames_data_categorical = pd.DataFrame()
videogames_data_categorical["Rating"] = videogames_data["Rating"]
videogames_data_categorical["Developer"] = videogames_data["Developer"]
videogames_data_categorical["Publisher"] = videogames_data["Publisher"]
videogames_data_categorical["Genre"] = videogames_data["Genre"]

videogames_data.drop("Name",1, inplace=True )
videogames_data.drop("Rating",1, inplace=True )
videogames_data.drop("Developer",1, inplace=True )
videogames_data.drop("Publisher",1, inplace=True )
videogames_data.drop("Genre",1, inplace=True )
videogames_data.drop("NA_Sales",1, inplace=True )
videogames_data.drop("JP_Sales",1, inplace=True )
videogames_data.drop("EU_Sales",1, inplace=True )
videogames_data.drop("Other_Sales",1, inplace=True )
videogames_data.drop("Global_Sales",1, inplace=True )
videogames_data.drop("Nominal_Critic_Score",1, inplace=True )
videogames_data.drop("Nominal_User_Score",1, inplace=True )
videogames_data.drop("Nominal_Global_Sales",1, inplace=True )
videogames_data.drop("Nominal_Other_Sales",1, inplace=True )
videogames_data.drop("Nominal_NA_Sales",1, inplace=True )
videogames_data.drop("Nominal_JP_Sales",1, inplace=True )
videogames_data.drop("Nominal_EU_Sales",1, inplace=True )

videogames_data_ordinal = videogames_data

#print( videogames_data_ordinal.describe() )
#print( )
#print( target.describe() )
pca = PCA(n_components=3)

pca_info = pca.fit(videogames_data_ordinal)

#print(pca_info.components_)
#print()

for explanation in pca_info.explained_variance_ratio_.cumsum():
   print(explanation)

videogames_data = pca.fit(videogames_data_ordinal).transform(videogames_data_ordinal)

csv_data = pd.DataFrame(videogames_data)
csv_data["Name"] = target["Name"].tolist()
csv_data["NA_Sales"] = target["NA_Sales"].tolist()
csv_data["JP_Sales"] = target["JP_Sales"].tolist()
csv_data["EU_Sales"] = target["EU_Sales"].tolist()
csv_data["Other_Sales"] = target["Other_Sales"].tolist()
csv_data["Global_Sales"] = target["Global_Sales"].tolist()
csv_data["Rating"] = videogames_data_categorical["Rating"].tolist()
csv_data["Developer"] = videogames_data_categorical["Developer"].tolist()
csv_data["Publisher"] = videogames_data_categorical["Publisher"].tolist()
csv_data["Genre"] = videogames_data_categorical["Genre"].tolist()

csv_data.to_csv("complete_processed_videogames_data.csv", index=False, header=True)

