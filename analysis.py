import pandas as pd
import math
import numpy as np

matrix = np.loadtxt('transition_matrix.csv', delimiter=',')
print(matrix)

df = pd.DataFrame(matrix, columns=['rain', 'clear'], index=['rain', 'clear'])

initial_state_rain = np.array([1,0]).reshape(2,1)
initial_state_clear = np.array([0,1]).reshape(2,1)

one_week_after_rain = df*initial_state_rain
one_week_after_clear = df*initial_state_clear

print("rain: \n", one_week_after_rain, ", \n", "clear: \n", one_week_after_clear)

