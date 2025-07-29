from fri_sat_sun_pattern_matrix import *
import numpy as np
import pandas as pd

def random_walk(transition_matrix, weeks, prediction):
    if prediction == "three_day":
        states_index = ["No rain", "Only Friday", "Only Saturday",
                        "Only Sunday", "Friday and Saturday",
                        "Friday and Sunday", "Saturday and Sunday",
                        "Rain all weekend"]
        state = 'Only Sunday'
        opts = 8
    else:
        states_index = ["No rain", "Rain"]
        state = 'Rain'
        opts = 2
    

    state_list = [state]

    # random walk
    i = 0
    while i != weeks:
        for j in range(len(states_index)):
            if state_list[-1] == states_index[j]:
                change = np.random.choice([x for x in range(opts)],replace=True,
                                          p=transition_matrix.iloc[j])
                
                state_list.append(states_index[change])
                break
               
        i += 1

    return state_list

def walk_probability(transition_matrix, weeks, prediction, mode, target):
    count = 0
    for i in range(100000):
        walk = random_walk(transition_matrix, weeks, prediction)
        if mode == "whole":
            if walk == target:
                count += 1
        elif mode == "last":
            if walk[-1] == target:
                count += 1
            
    percentage = (count/100000) * 100

    print(f"The probability of the observed weather pattern according to the given matrix is {percentage}%")

def main():
    matrix = pd.read_csv('2x2.csv', index_col=0, header=0)
    print(matrix.iloc[0])
    walk_probability(matrix, 5, "whole", 'whole', ['Rain', 'Rain',
                                                   'No rain', 'No rain',
                                                   'Rain', 'Rain'])
    

if __name__ == "__main__":
    main()
