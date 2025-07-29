# https://timeseriesreasoning.com/contents/introduction-to-discrete-time-markov-processes/
import random
import math
import numpy as np
import matplotlib.pyplot as plt

from transition_matrix_weekend import weather_row_norm

# Simulate a given day (choosing rain)
weather = 1

# initialize pi_0
pi_0 = np.array([0.5, 0.5])

# create a random delta in the range [0, 1.0]
delta = random.random() * 1

# generate a random number in the range [0.0, 1.0]
r = random.random()

# if r <= P(X_t = 1), increase the probability of rain by events + 1/event space so far,
# else decrease the closing price by delta
i = 1 # event space
r = 0 # times predicting rain
n = 0 # times predicting no rain
if r <= pi_0[0]:
    weather = weather * (1 + delta) / 1
else:
    weather = max(weather * (1 - delta) / 1, 1.0)

# accumulate the new closing price
weather_pattern = [weather]
print(weather_pattern)

weekend_mul = weekend_only.copy()
T = 100

# now repeat this procedure 365 times
for w in range(T):
    # calculate the i-step transition matrix P^i
    weekend_mul = np.matmul(weekend_mul, weekend_only)
    # multiply it by pi_0 to get the state probability for time i
    pi_t = np.matmul(pi_0, weekend_mul)
    # create a random delta in the range [0, 2.0]
    delta = random.random() * 2
    # generate a random number in the range [0.0, 1.0]
    r = random.random()
    # if r <= P(X_t = +1), increase the closing price by delta,
    # else decrease the closing price by delta
    if r <= pi_t[0]:
        weather = max(weather * (1 + delta) / 1, 1.0)
    else:
        weather = weather * (1 - delta) / 1
    # accumulate the new closing price
    weather_pattern.append(weather)

# plot all the accumulated closing prices
fig = plt.figure()
fig.suptitle('probability of rain throughout the year')
plt.xlabel('time t')
plt.ylabel('rain probability')
plt.plot(range(T + 1), weather_pattern)
plt.show()