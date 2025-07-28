from fri_sat_sun_pattern_matrix import *
import numpy as np
import pandas as pd

def random_walk(transition_matrix, weeks, prediction="whole"):
    if prediction == "three_day":
        states_index = ["No rain", "Only Friday", "Only Saturday",
                        "Only Sunday", "Friday and Saturday",
                        "Friday and Sunday", "Saturday and Sunday",
                        "Rain all weekend"]
        state = 'Only Sunday'
    else:
        states_index = ["Rained", "Clear"]
        states = 'Rained'
    

    state_list = [state]

    # random walk
    i = 0
    while i != weeks:
        for j in range(len(states_index)):
            if state_list[-1] == states_index[j]:
                change = np.random.choice([x for x in range(8)],replace=True,
                                          p=transition_matrix.iloc[j])
                
                state_list.append(states_index[change])
                break
               
        i += 1

    return state_list

def walk_probability(transition_matrix, weeks=5, prediction="whole"):
    count = 0
    for i in range(100000):
        walk = random_walk(transition_matrix, weeks, prediction)
        if walk == ['Only Sunday', 'Only Saturday', 'No rain', 'No rain',
                    'Only Sunday', 'Friday and Sunday']:
            count += 1
            
    percentage = (count/100000) * 100

    print(f"The probability of the observed weather pattern according to the given matrix is {percentage}%")

def main():
    df = weekends_grid('rain_data_5y.csv',
                       ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday'])
    matrix = stochastic_matrix(df['State'].tolist())
    matrix.to_csv('matrix')
    walk_probability(matrix, 5, "three_day")

if __name__ == "__main__":
    main()
