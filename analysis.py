import pandas as pd
import math
import numpy as np

matrix = np.loadtxt('transition_matrix.csv', delimiter=',')
print(matrix)

df = pd.DataFrame(matrix, columns=['rain', 'clear'], index=['rain', 'clear'])

# must rain on first day = 1,0.
initial_state_rain = np.array([1,0]).reshape(2,1)

# must NOT rain on first day = 0,1.
initial_state_clear = np.array([0,1]).reshape(2,1)

# 10/90 chance = .9, .1.
initial_state_nine_to_one = np.array([.9,.1]).reshape(2,1)

# 50/950 chance = .5, .5.
initial_state_half = np.array([.5,.5]).reshape(2,1)

one_week_after = df*initial_state_nine_to_one
two_weeks_after = (df**2)*initial_state_nine_to_one

print("one week: \n", one_week_after, ", \n", "two weeks: \n", two_weeks_after)

one_week_after = df*initial_state_half
two_weeks_after = (df**2)*initial_state_half

print("one week: \n", one_week_after, ", \n", "two weeks: \n", two_weeks_after)