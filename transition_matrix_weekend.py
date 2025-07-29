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
print(weather)

# June 24 2024 was a Monday, 52 * 7 is 364, Q = day of week, W = weekend or Friday
weather["day_of_week"] = ["Q", "Q", "Q", "Q", "W", "W", "W"]*(365/7).__floor__() + ["Q", "Q"]
weather["together"] = weather["precipitation"].astype("string") + "," + weather["day_of_week"]
weather_list = weather["together"].tolist()

print(weather_list)
weather.to_csv('total_weather_data.csv', index=True)

#https://medium.com/data-science/time-series-data-markov-transition-matrices-7060771e362b

def get_tuples_week(list):
    """converts list of weather patterns into a collection of week-long tuples"""
    return [(list[i], list[i+1], list[i+2], list[i+3], list[i+4], list[i+5], list[i+6]) for i in range(0, len(list)-6, 7)]

def get_transition_tuples_week_to_week(list):
    """converts list of weather patterns into a collection of week-to_week tuples"""
    return [(list[i], list[i+1]) for i in range(0, len(list)-1)]

def get_transition_state(tuple_list):
    """converts list of tuples into transition states. The transition state
    is indicative of whether it rained AT ALL on a given weekend."""
    transition_event = "off_week"

    # rain on a given weekend (friday inclusive) yes/no. TIME POINT MUST START ON A MONDAY
    if tuple_list[0] == "1,Q" or tuple_list[0] == "0,Q":
        pass
        if tuple_list[1] == "1,Q" or tuple_list[1] == "0,Q":
            pass
            if tuple_list[2] == "1,Q" or tuple_list[2] == "0,Q":
                pass
                if tuple_list[3] == "1,Q" or tuple_list[3] == "0,Q":
                    pass
                    if tuple_list[4] == "0,W" and tuple_list[5] == "0,W" and tuple_list[6] == "0,W":
                        transition_event = "clear_weekend"
                    else:
                        transition_event = "rain_weekend"
    return transition_event

# formally getting tuple list from data
weather_tuples = get_tuples_week(weather_list)
print("tup len", len(weather_tuples))

# formally getting transition states from tuples
weather_transitions = [get_transition_state(tuples) for tuples in weather_tuples]
print(weather_transitions, "\n",
      "transition len", len(weather_transitions))

# getting discrete transitions in tuple form
weather_transitions_week_to_week = get_transition_tuples_week_to_week(weather_transitions)
print("transition len", len(weather_transitions_week_to_week), "\n", weather_transitions_week_to_week)

# indexes
weather_indexes = ["clear_weekend", "rain_weekend"]

# dataframe
weather_df = pd.DataFrame(0, index=weather_indexes, columns=weather_indexes)

# filling df
for a,b in weather_transitions_week_to_week:
    weather_df.loc[a,b] += 1
print(weather_df)

# normalizing matrix, question: row or column normalization
weather_row_norm = weather_df.div(weather_df.sum(axis = 1), axis = 0).fillna(0.00)
print(weather_row_norm)


### uncomment to get csv versions of these dataframes
# weather_df.to_csv('csv/weather_transition.csv', index=True)
# np.savetxt('csv/transition_matrix.csv', weather_row_norm, delimiter=',')
