import pandas as pd
import numpy as np

videogames_data = pd.read_csv("processed_videogames_data.csv")
print(videogames_data.loc[(videogames_data["Critic_Score"] == 0.0) & (videogames_data["User_Score"] == 0.0)].count())
videogames_data["User_Count"] = videogames_data["User_Count"].astype(int)
videogames_data["Year_of_Release"] = videogames_data["Year_of_Release"].astype(int)
videogames_data["Critic_Count"] = videogames_data["Critic_Count"].astype(int)

videogames_data.drop('Platform', 1, inplace=True)
print(videogames_data["User_Score"].sum()/videogames_data["Name"][(videogames_data["User_Score"] > 0.0 ) ].count())

print(videogames_data["Name"][(videogames_data["User_Score"] == 0.0 ) & (videogames_data["Critic_Score"] == 0.0 ) ].count() )