import pandas as pd
import math
import numpy as np

from data_loading import rain_data

weather = rain_data.copy()

weather.rename(columns = {"prcp": "precipitation"}, inplace = True)

print(weather)

### cleaning weather data ###

# if it rained at all, set the column value to 1, else 0
weather["precipitation"] = weather["precipitation"].apply(lambda x: 1 if x > 0 else 0)
#print(weather)

# June 24 2024 was a Monday, 52 * 7 is 364, Q = day of week, W = weekend or Friday
weather["day_of_week"] = ["Q", "Q", "Q", "Q", "W", "W", "W"]*(365/7).__floor__() + ["Q", "Q"]
weather["together"] = weather["precipitation"].astype("string") + "," + weather["day_of_week"]
weather_list = weather["together"].tolist()

#https://medium.com/data-science/time-series-data-markov-transition-matrices-7060771e362b

def get_transition_tuples(list):
    """converts list of weather patterns into a collection of two-day tuples"""
    return [(list[i - 1], list[i]) for i in range(1, len(list))]

def get_transition_state(tuple_list):
    """converts list of tuples into transition states"""
    transition_event = "no_change"
    if tuple_list[0] == "1,Q" and tuple_list[1] == "1,Q":
        transition_event = "rained_Q"
    if tuple_list[0] == "0,Q" and tuple_list[1] == "1,Q":
        transition_event = "rained_Q"
    if tuple_list[0] == "1,Q" and tuple_list[1] == "0,Q":
        transition_event = "cleared_Q"
    if tuple_list[0] == "0,Q" and tuple_list[1] == "0,Q":
        transition_event = "cleared_Q"
    if tuple_list[0] == "1,Q" and tuple_list[1] == "0,W": # because this does not tell us about the whole weekend
        transition_event = "cleared_Q"
    if tuple_list[0] == "0,Q" and tuple_list[1] == "0,W": # because this does not tell us about the whole weekend
        transition_event = "cleared_Q"
    if tuple_list[0] == "1,Q" and tuple_list[1] == "1,W":
        transition_event = "rained_W"
    if tuple_list[0] == "0,Q" and tuple_list[1] == "1,W":
        transition_event = "rained_W"
    if tuple_list[0] == "0,W" and tuple_list[1] == "1,W": # bc weekend included a rain event
        transition_event = "rained_W"
    if tuple_list[0] == "0,W" and tuple_list[1] == "0,W": # whole weekend not raining
        transition_event = "clear_W"
    if tuple_list[0] == "1,W" and tuple_list[1] == "1,W": # bc weekend included a rain event
        transition_event = "rained_W"
    if tuple_list[0] == "1,W" and tuple_list[1] == "0,W": # bc weekend included a rain event
        transition_event = "rained_W"
    if tuple_list[0] == "0,W" and tuple_list[1] == "1,Q":
        transition_event = "rained_Q"
    if tuple_list[0] == "1,W" and tuple_list[1] == "1,Q":
        transition_event = "rained_Q"
    if tuple_list[0] == "0,W" and tuple_list[1] == "0,Q":
        transition_event = "cleared_Q"
    if tuple_list[0] == "1,W" and tuple_list[1] == "0,Q":
        transition_event = "cleared_Q"
    return(transition_event)

# formally getting tuple list from data
weather_tuples = get_transition_tuples(weather_list)

# formalling getting transition states from tuples
weather_transitions = [get_transition_state(tuples) for tuples in weather_tuples]
#print(weather_transitions, len(weather_transitions))

# getting discrete transitions in tuple form
weather_transitions_per_day = get_transition_tuples(weather_transitions)
#print(weather_transitions_per_day)

# indexes
weather_indexes = ["rained_Q", "cleared_Q", "rained_W", "clear_W"]

# dataframe
weather_df = pd.DataFrame(0, index=weather_indexes, columns=weather_indexes)

# filling df
for a,b in weather_transitions_per_day:
    weather_df.loc[a,b] += 1
#print(weather_df)

# normalizing matrix, question: row or column normalization
weather_row_norm = weather_df.div(weather_df.sum(axis = 1), axis = 0).fillna(0.00)
#print(weather_row_norm)

# turning into array
weather_array = np.array(weather_row_norm)
print(weather_row_norm)

# shrinking the array so that only weekend data is included
weekend_only = weather_array[2:4, 2:4]
print(weekend_only)
