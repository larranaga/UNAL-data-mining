import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


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


videogames_data["Rating"] = pd.factorize(videogames_data["Rating"])[0]
videogames_data["Developer"] = pd.factorize(videogames_data["Developer"])[0]
videogames_data["Publisher"] = pd.factorize(videogames_data["Publisher"])[0]
videogames_data["Genre"] = pd.factorize(videogames_data["Genre"])[0]
names = videogames_data["Name"]

videogames_data.drop("Name",1, inplace=True )
print(videogames_data.shape)
pca = PCA(n_components=8)

videogames_data = pca.fit(videogames_data).transform(videogames_data)

print(videogames_data.shape)

#videogames_data.to_csv("processed_videogames_data_4.csv", index=False)