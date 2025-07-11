import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from transition_matrix import weather

print(weather)

fig, ax = plt.subplots()
ax.bar([0,1], weather["precipitation"].value_counts(), label = ["No rain", "Rain"], color = ['black', 'gray'])

ax.set_ylabel('Count')
ax.set_title('Days of the year (June 2024 -- June 2025) it rained or did not in Boston')
ax.legend(title='Rained or Not (Daily)')

plt.show()