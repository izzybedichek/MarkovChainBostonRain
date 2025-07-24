import pandas as pd
import numpy as np
from fri_sat_sun_pattern_matrix import weekends_condensed, transition_matrix

# data frame representing weekends from June 2th-July 23rd
weather_june_july = pd.DataFrame({'Start Date': ['2025-06-27', '2025-07-04', '2025-07-11', '2025-07-18'],
                                  'Real Weather': ['Only Friday', 'No rain', 'No rain', 'No rain']})

print('Initial state:' + weekends_condensed.loc[51, 'State'])
# Output: 'Only Sunday'

initial_state = np.array([0, 0, 0, 1, 0, 0, 0, 0])

prediction = [initial_state]

for i in range(4):  
    prediction.append(prediction[-1] @ transition_matrix)


prediction_df = pd.DataFrame(prediction, columns=["No rain", "Only Friday", "Only Saturday", "Only Sunday",
                                                  "Friday and Saturday", "Friday and Sunday",
                                                  "Saturday and Sunday", "Rain all weekend"])

print(prediction_df)

most_likely = prediction_df.idxmax(axis=1).drop(index=0).reset_index(drop=True)

print(most_likely)

weather_june_july['Predicted'] = most_likely

print(weather_june_july)

