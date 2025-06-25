# pip install meteostat in terminal
from meteostat import Point, Daily

# source for lat, long, altitude (in meters): https://wiki.openstreetmap.org/wiki/Boston,_Massachusetts#:~:text=Boston%20is%20a%20city%20in,°05′09.96″%20West.
# https://en.wikipedia.org/wiki/Boston
boston = Point( 42.3736, -71.0861, 14)

start_date = datetime(2024, 6, 24)
end_date = datetime(2025, 6, 24)

boston_weather = Daily(boston, start, end)
boston_weather = boston_weather.fetch()