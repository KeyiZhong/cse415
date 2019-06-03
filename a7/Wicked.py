'''Wicked.py
'''
# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Wicked Problem"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Keyi Zhong, Huixin Lai']
PROBLEM_CREATION_DATE = "28-MAY-2019"
PROBLEM_DESC = \
    '''This formulation is a simulation of global refugee issues in real world.
    '''
# </METADATA>

# <COMMON_DATA>
'http://popstats.unhcr.org/en/overview#_ga=2.224905497.2002459104.1559515164-74010300.1559515164'
TOTAL_NUM_OF_REFUGEES = 20000000
# need more countries
COUNTRIES = ['USA','UK','Germany','France','Russia','China']
''''# of refugee', World stats, current number, https://data.worldbank.org/indicator/sm.pop.refg
    'GDP', world stats, https://www.worldometers.info/gdp/#top20
    'public security', safety index, https://www.numbeo.com/crime/rankings_by_country.jsp
    'political stability', number of parties, 1 - 100, 2 - 80, 3 - 60 and the rest are 40 
    https://en.wikipedia.org/wiki/List_of_ruling_political_parties_by_country
    'honor', 0 as a default
'''
ATTRIBUTES = ['# of refugee', 'GDP', 'public security', 'political stability', 'honor']
POSSIBLE_ACTION = ['lowers number of refugees',
                   'increases number of refugees',
                   'sends military force to refugees country',
                   'cancels refugees policy',
                   'starts refugees policy']
# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self):
        self.b = INITIAL_STATE

    def __eq__(self, s2):
        for country in self.b:
            if country not in s2.b:
                return False
            if self.b[country] != s2.b[country]:
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        total_num = 0
        countries = self.b
        for country in countries:
            total_num += int(countries[country]['# of refugee'])
        result = "\nTOTAL NUMBER OF REFUGEES = "+ str(TOTAL_NUM_OF_REFUGEES) +\
                 "\nrefugees accepted = " + str(total_num) + "\n"
        for country in self.b:
            result = result + country + ":\n"
            for value in self.b[country]:
                result = result + "    " + value + ": " + str(self.b[country][value]) +"\n"
        return result

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State()
        news.b = self.b.copy()
        return news

    def can_move(self, act):
        ''''lower number of refugees' need country's political stability >= 60, or honor < 10
            'increase number of refugees' need country's political stability >= 60, or GDP > 30
            'send military force to refugees country' need GDP > 50 or public security > 60
            'cancel refugees policy' need honor > 10, GDP < 40, number of refugees != 0, political stability > 70
            'start refugees policy' political stability >= 60, number of refugees == 0
        '''
        country = str.split(act)[0]
        action = str.split(act)[1]
        for attribute in ATTRIBUTES:
            if self.b[country][attribute] < 0:
                return False
        if action == "lowers":
            if self.b[country]["political stability"] >= 30 or self.b[country]["honor"] < 10 and self.b[country]["# of refugee"] >= 10000:
                return True
        elif action == "increases":
            if self.b[country]["political stability"] >= 60 or self.b[country]["GDP"] > 30 and self.b[country]["# of refugee"] != 0:
                return True
        elif action == "sends":
            if self.b[country]["GDP"] > 50 and self.b[country]["public security"] > 60:
                return True
        elif action == "cancels":
            if self.b[country]["honor"] > 10 or self.b[country]["GDP"] < 40 or \
                    self.b[country]["political stability"] > 70 and self.b[country]["# of refugee"] != 0:
                return True
        elif action == "starts":
            if self.b[country]["political stability"] >= 60 and self.b[country]["# of refugee"] == 0:
                return True
        return False

    def move(self, act):
        '''
        'lower number of refugees' - 1/10 refugees, + 5 public security, + 10 GDP, + 5 political stability
        'increase number of refugees' + 1/10 refugees, - 5 public security, - 5 GDP, - 5 political stability, + 1 honor
        'send military force to refugees country' - 1/10 TOTAL refugee, + 8 political , - 7 public security, - 10 GDP, + 1 honor
        'cancel refugees policy' refugees = 0, + 10 public security, - 10 political stability
        'start refugees policy' + 1/50 refugees, + 3 honor
        '''
        country = str.split(act)[0]
        action = str.split(act)[1]
        news = self.copy()
        if action == "lowers":
            news.b[country]["# of refugee"] -= int(news.b[country]["# of refugee"] / 3)
            news.b[country]["public security"] += 5
            news.b[country]["GDP"] += 10
            news.b[country]["political stability"] += 5
        elif action == "increases":
            news.b[country]["# of refugee"] += int(news.b[country]["# of refugee"] / 3)
            news.b[country]["public security"] -= 5
            news.b[country]["GDP"] -= 5
            news.b[country]["political stability"] -= 5
            news.b[country]["honor"] += 1
        elif action == "sends":
            global TOTAL_NUM_OF_REFUGEES
            TOTAL_NUM_OF_REFUGEES -= int(TOTAL_NUM_OF_REFUGEES / 10)
            news.b[country]["political stability"] += 8
            news.b[country]["public security"] -= 7
            news.b[country]["GDP"] -= 10
            news.b[country]["honor"] += 1
        elif action == "cancels":
            news.b[country]["# of refugee"] = 0
            news.b[country]["public security"] += 10
            news.b[country]["political stability"] -= 10
        elif action == "starts":
            news.b[country]["# of refugee"] = int(TOTAL_NUM_OF_REFUGEES / 50)
            news.b[country]["honor"] += 3
        return news

    def edge_distance(self,s):
        total_num = 0
        countries = s.b
        for country in countries:
            total_num += int(countries[country]['# of refugee'])
        return TOTAL_NUM_OF_REFUGEES - total_num



def goal_test(s):
    '''If total refugee is greater or equal to the number of refugee in real world'''
    total_num = 0
    countries = s.b
    for country in countries:
        total_num += int(countries[country]['# of refugee'])
    return total_num > TOTAL_NUM_OF_REFUGEES


def goal_message(s):
    return "You have solved the world problem"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
# Use default, but override if new value supplied
# by the user on the command line.
# try:
#     import sys
#
#     init_state_string = sys.argv[2]
#     print("Initial state as given on the command line: " + init_state_string)
#     init_state_list = eval(init_state_string)
# except:
#     init_state_list = [[3, 1, 2], [0, 5, 8], [4, 6, 7]]
#     print("Using default initial state list: " + str(init_state_list))
#     print(" (To use a specific initial state, enter it on the command line, e.g.,")
#     print("python3 UCS.py EightPuzzle '[[3, 1, 2], [0, 4, 5], [6, 7, 8]]'")

CREATE_INITIAL_STATE = lambda: State()


def default_country():
    country = {}
    for attribute in ATTRIBUTES:
        country[attribute] = 0
    return country


def create_country(nor,gdp, public, political,honor):
    country = {}
    country['# of refugee'] = nor
    country['GDP'] = gdp
    country['public security'] = public
    country['political stability'] = political
    country['honor'] = honor
    return country


# need to define default number
def default_state():
    status = {}
    for country in COUNTRIES:
        if country == 'USA':
            status['USA'] = create_country(287065,194,53,80,0)
        if country == 'UK':
            status['UK'] = create_country(121766,26,57,80,0)
        if country == 'Germany':
            status['Germany'] = create_country(970302,36,65,40,0)
        if country == 'France':
            status['France'] = create_country(337143,25,53,40,0)
        if country == 'Russia':
            status['Russia'] = create_country(125986,15,58,80,0)
        if country == 'China':
            status['China'] = create_country(321699,122,54,100,0)
    return status


INITIAL_STATE = default_state()
# </INITIAL_STATE>

# <OPERATORS>
ACTION = [(country + " " + action) for country in COUNTRIES for action in POSSIBLE_ACTION]
OPERATORS = [Operator(act,
                      lambda s, act1=act: s.can_move(act1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s, act1=act: s.move(act1))
             for act in ACTION]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

