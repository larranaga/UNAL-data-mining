import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


videogames_data = pd.read_csv("complete_processed_nominal_videogames_data.csv")

print(videogames_data["Name"][videogames_data["Nominal_JP_Sales"] == "error"])
