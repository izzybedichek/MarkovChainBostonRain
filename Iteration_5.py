### Initial findings or test runs ###

# the initial findings were in an attached csv file called transition_matrix.csv
# It is the transition matrix created from data

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


# Discuss how these early results might shape your further analysis: comparing more years

""""""

### Refine Implementation ###

# Begin preparing visualizations of your results.
"""in class example of graphing probabilities"""