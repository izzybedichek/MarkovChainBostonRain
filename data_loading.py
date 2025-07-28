# pip install meteostat in terminal
from datetime import datetime
from meteostat import Point, Daily

# source for lat, long, altitude (in meters): https://wiki.openstreetmap.org/wiki/Boston,_Massachusetts#:~:text=Boston%20is%20a%20city%20in,°05′09.96″%20West.
# https://en.wikipedia.org/wiki/Boston
boston = Point( 42.3736, -71.0861, 14)

# setting the time to be approximately a calendar year
start_date = datetime(2024, 6, 24)
end_date = datetime(2025, 6, 24)

#start_date = datetime(2020, 6, 24)
#end_date = datetime(2025, 6, 24)

# getting daily weather data
boston_weather = Daily(boston, start_date, end_date)
boston_weather = boston_weather.fetch()

# copying the data frame for best practice data handling
weather_data = boston_weather.copy()

# checking the output
print(weather_data)

# taking only precipitation and datetime, resetting index so that datetime is considered a column rather than an index
rain_data = weather_data[["prcp"]].reset_index()

# checking the output
print(rain_data)

rain_data.to_csv("rain_data.csv", index = True)