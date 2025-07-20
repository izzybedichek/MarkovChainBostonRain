import pandas as pd
import math
import numpy as np

from transition_matrix import *

matrix = weekend_only.copy()


initial_state_rain = np.array([1,0])
initial_state_clear = np.array([0,1])

one_week_after_rain = matrix*initial_state_rain
one_week_after_clear = matrix*initial_state_clear

print("rain: ", one_week_after_rain, ",", "clear: ", one_week_after_clear)

