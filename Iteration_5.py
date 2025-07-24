
### All of iteration 5 is in this document

### Initial Findings: ###

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from meteostat import Point, Daily

# source for lat, long, altitude (in meters): https://wiki.openstreetmap.org/wiki/Boston,_Massachusetts#:~:text=Boston%20is%20a%20city%20in,°05′09.96″%20West.
# https://en.wikipedia.org/wiki/Boston
boston = Point( 42.3736, -71.0861, 14)

# getting data from Jan - June 2024 and 2025, respectively
start_date_24 = datetime(2024, 1, 1)
end_date_24 = datetime(2024, 6, 30)

start_date_25 = datetime(2025, 1, 1)
end_date_25 = datetime(2025, 6, 30)

weather_24 = Daily(boston, start_date_24, end_date_24)
weather_24 = weather_24.fetch()

weather_25 = Daily(boston, start_date_25, end_date_25)
weather_25 = weather_25.fetch()

# copying the data frame for best practice data handling
weather_25_copy = weather_25.copy()
weather_24_copy = weather_24.copy()

# isolating rain data
rain_24 = weather_24_copy[["prcp"]].reset_index()
rain_25 = weather_25_copy[["prcp"]].reset_index()

# If need .csv files, uncomment:
# rain_24.to_csv("rain_24.csv", index = True)
# rain_25.to_csv("rain_25.csv", index = True)

rain_24.rename(columns = {"prcp": "precipitation"}, inplace = True)
rain_25.rename(columns = {"prcp": "precipitation"}, inplace = True)

# if it rained at all, set the column value to 1, else 0
rain_24["precipitation"] = rain_24["precipitation"].apply(lambda x: 1 if x > 0 else 0)
rain_25["precipitation"] = rain_25["precipitation"].apply(lambda x: 1 if x > 0 else 0)

# First day of 2024 was a Monday, first day of 2025 was a Wednesday
rain_24["day_of_week"] = (["Q", "Q", "Q", "Q", "W", "W", "W"]*(len(rain_24)/7).__floor__())
rain_24["together"] = rain_24["precipitation"].astype("string") + "," + rain_24["day_of_week"]
twenty_four_list = rain_24["together"].tolist()

rain_25["day_of_week"] = (["Q", "Q", "Q", "Q", "W", "W", "W"]*(len(rain_25)/7).__floor__() + ["Q", "Q", "Q", "Q", "W", "W"])
rain_25["together"] = rain_25["precipitation"].astype("string") + "," + rain_25["day_of_week"]
twenty_five_list = rain_25["together"].tolist()

""" Compare transition matrices of the first 6 months of 2024, 2025"""

from transition_matrix_weekend import get_transition_tuples, get_transition_state

# formally getting tuple list from data
t_four_tuples = get_transition_tuples(twenty_four_list)
t_five_tuples = get_transition_tuples(twenty_five_list)

# formally getting transition states from tuples
t_four_transitions = [get_transition_state(tuples) for tuples in t_four_tuples]
t_five_transitions = [get_transition_state(tup) for tup in t_five_tuples]

# getting discrete transitions in tuple form
weather_transitions_per_day_24 = get_transition_tuples(t_four_transitions)
weather_transitions_per_day_25 = get_transition_tuples(t_five_transitions)

# indexes
weather_indexes = ["rained_Q", "cleared_Q", "rained_W", "clear_W"]

# dataframe
df_24 = pd.DataFrame(0, index=weather_indexes, columns=weather_indexes)
df_25 = df_24.copy()

# filling df (2024)
for a,b in weather_transitions_per_day_24:
    df_24.loc[a,b] += 1
print(df_24)

# filling df (2025)
for a,b in weather_transitions_per_day_25:
    df_25.loc[a,b] += 1
print("25:", df_25)

# normalizing matrix, question: row or column normalization
weather_row_norm_24 = df_24.div(df_24.sum(axis = 1), axis = 0).fillna(0.00)
weather_row_norm_25 = df_25.div(df_25.sum(axis = 1), axis = 0).fillna(0.00)

# turning into array
array_24 = np.array(weather_row_norm_24)
array_25 = np.array(weather_row_norm_25)
print(weather_row_norm_24)
print(weather_row_norm_25)

weekend_only_24 = array_24[2:4, 2:4]
weekend_only_25 = array_25[2:4, 2:4]
print(weekend_only_24, "\n", weekend_only_25)

print("Probability of rain after rain \n", "2024:", weekend_only_24[0,0], "vs",
      "2025:", weekend_only_25[0,0],
      "\n Probability of clear after rain \n", "2024:", weekend_only_24[0,1], "vs",
      "2025:", weekend_only_25[0,1], "\n",
      "\n Probability of rain after clear \n", "2024:", weekend_only_24[1,0], "vs",
      "2025:", weekend_only_25[1,0], "\n",
      "\n Probability of clear after clear \n", "2024:", weekend_only_24[1,1], "vs",
      "2025:", weekend_only_25[1,1])

### Discuss how these early results might shape your further analysis: ###

"""
These results show a distinct difference in likelihood to rain from weekend to weekend based on year.
This result makes us want to look at more years and see if there's a pattern as well as if the
stationary distributions are different


 Probability of rain after rain 
 2024: 0.5454545454545454 vs 2025: 0.5757575757575758 
 Probability of clear after rain 
 2024: 0.06818181818181818 vs 2025: 0.09090909090909091 
 
 Probability of rain after clear 
 2024: 0.1875 vs 2025: 0.07407407407407407 
 
 Probability of clear after clear 
 2024: 0.3125 vs 2025: 0.4074074074074074
 """

### Refine Implementation ###

# Inspiration for code:
# https://ninavergara2.medium.com/calculating-stationary-distribution-in-python-3001d789cd4b
# https://datascience.oneoffcoder.com/markov-chain-stationary-distribution.html

transition_matrix_t_24 = weekend_only_24.T
transition_matrix_t_25 = weekend_only_25.T

eigenvals_24, eigenvects_24 = np.linalg.eig(transition_matrix_t_24)
eigenvals_25, eigenvects_25 = np.linalg.eig(transition_matrix_t_25)

"""close_to_1_idx = np.isclose(eigenvals,1)
target_eigenvect = eigenvects[:,close_to_1_idx]
target_eigenvect = target_eigenvect[:,0]
# Turn the eigenvector elements into probabilites
stationary_distrib = target_eigenvect / sum(target_eigenvect)"""

# Begin preparing visualizations of your results.
G = nx.MultiDiGraph(time = "weekend")
nx.circular_layout(G)
subax1 = plt.subplot(212)
G.add_weighted_edges_from([("rain", "clear", 0.5), ("clear", "rain", 0.75)])
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()