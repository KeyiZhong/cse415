from Wicked import *

def h(s):
    '''Heuristic function
    moves needed for country with lowest number of refugees to "increase" to meet the goal'''
    countries = s.b
    highestCountry = 'USA'
    for country in countries:
        if int(countries[country]['# of refugee']) > int(countries[highestCountry]["# of refugee"]):
            highestCountry = country
    nor = int(countries[highestCountry]["# of refugee"])
    step = 0
    if nor == 0:
        nor += TOTAL_NUM_OF_REFUGEES / 10
        step += 1
    while nor < TOTAL_NUM_OF_REFUGEES:
        nor += nor / 3
        step += 1
    return step