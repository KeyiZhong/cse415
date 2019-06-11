from Wicked import *

def h(s):
    '''Heuristic function
    moves needed for country with lowest number of refugees to "increase" to meet the goal'''
    step = 0
    total_number = TOTAL_NUM_OF_REFUGEES
    current_total = total(s)
    while current_total < total_number:
        total_number -= total_number/10
        step +=1
    return step