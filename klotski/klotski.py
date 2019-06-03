'''klotski.py
'''
# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Klotski Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Keyi Zhong, Huixin Lai']
PROBLEM_CREATION_DATE = "27-MAY-2019"
PROBLEM_DESC = \
    '''This formulation of the Eight Puzzle uses generic
    Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.
    '''
# </METADATA>
DEFAULT_INITIAL_STATE = [[2, 1, 1, 3],
                 [2, 1, 1, 3],
                 [4, 6, 6, 5],
                 [4, 7, 8, 5],
                 [9, 0, 0, 10]]

# <COMMON_DATA>
# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self, b):
        if len(b) == 5 and len(b[0]) == 4:
            self.b = b
        else:
            self.b = DEFAULT_INITIAL_STATE

    def __eq__(self, s2):
        for i in range(5):
            for j in range(4):
                if self.b[i][j] != s2.b[i][j]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "\n["
        for i in range(5):
            txt += str(self.b[i]) + "\n "
        return txt[:-2] + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.b = [row[:] for row in self.b]
        return news

    def find_void_location(self):
        '''Return the (vi, vj) coordinates of the void.
        vi is the row index of the void, and vj is its column index.'''
        void = []
        for i in range(5):
            for j in range(4):
                if self.b[i][j] == 0:
                    void.append((i, j))
        raise Exception("No void location in state: " + str(self))

    def find_target_location(self, p):
        pieces = []
        for i in range(5):
            for j in range(4):
                if self.b[i][j] == p:
                    pieces.append((i, j))
        return pieces

    def can_move(self, p, dir):
        '''Tests whether it's legal to move a tile that is next
           to the void in the direction given.'''
        pieces = self.find_target_location(p)
        b = self.b
        can = True
        for (i, j) in pieces:
            if dir == 'N':
                if i - 1 < 0:
                    can = False
                if i - 1 >= 0 and b[i - 1][j] != 0 and b[i - 1][j] != p:
                    can = False
            if dir == 'S':
                if i + 1 >= len(b):
                    can = False
                if i + 1 < len(b) and b[i + 1][j] != 0 and b[i + 1][j] != p:
                    can = False
            if dir == 'E':
                if j + 1 >= len(b[0]):
                    can = False
                if j + 1 < len(b[0]) and b[i][j + 1] != 0 and b[i][j + 1] != p:
                    can = False
            if dir == 'W':
                if j - 1 < 0:
                    can = False
                if j - 1 >= 0 and b[i][j - 1] != 0 and b[i][j - 1] != p:
                    can = False
        return can

    def move(self, p, dir):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from moving a tile in the
           given direction, into the void.'''
        news = self.copy()  # start with a deep copy.
        b = news.b
        pieces = self.find_target_location(p)
        if dir == 'N':
            try:
                for (i, j) in pieces:
                    if b[i - 1][j] == 0:
                        if i + 1 < 5:
                            if b[i + 1][j] == p:
                                b[i - 1][j] = p
                                b[i + 1][j] = 0
                            else:
                                b[i - 1][j] = p
                                b[i][j] = 0
                        else:
                            b[i - 1][j] = p
                            b[i][j] = 0
            except IndexError:
                raise Exception("Illegal direction for " + str(p) + " in direction: " + str(dir))
        if dir == 'S':
            try:
                for (i, j) in pieces:
                    if b[i + 1][j] == 0:
                        if i - 1 >= 0:
                            if b[i - 1][j] == p:
                                b[i + 1][j] = p
                                b[i - 1][j] = 0
                            else:
                                b[i + 1][j] = p
                                b[i][j] = 0
                        else:
                            b[i + 1][j] = p
                            b[i][j] = 0
            except IndexError:
                raise Exception("Illegal direction for " + str(p) + " in direction: " + str(dir))
        if dir == 'W':
            try:
                for (i, j) in pieces:
                    if b[i][j - 1] == 0:
                        if j + 1 < 4:
                            if b[i][j + 1] == p:
                                b[i][j - 1] = p
                                b[i][j + 1] = 0
                            else:
                                b[i][j - 1] = p
                                b[i][j] = 0
                        else:
                            b[i][j - 1] = p
                            b[i][j] = 0
            except IndexError:
                raise Exception("Illegal direction for " + str(p) + " in direction: " + str(dir))
        if dir == 'E':
            try:
                for (i, j) in pieces:
                    if b[i][j + 1] == 0:
                        if j - 1 >= 0:
                            if b[i][j - 1] == p:
                                b[i][j + 1] = p
                                b[i][j - 1] = 0
                            else:
                                b[i][j + 1] = p
                                b[i][j] = 0
                        else:
                            b[i][j + 1] = p
                            b[i][j] = 0
            except IndexError:
                raise Exception("Illegal direction for " + str(p) + " in direction: " + str(dir))
        return news  # return new state

    def edge_distance(self, s2):
        return 1.0  # Warning, this is only correct when
        # self and s2 are neighboring states.
        # We assume that is the case.  This method is
        # provided so that problems having all move costs equal to
        # don't have to be handled as a special case in the algorithms.


def goal_test(s):
    '''If all the b values are in order, then s is a goal state.'''
    b = s.b
    return b[4][1] == 1 and b[4][2] == 1 and b[3][1] == 1 and b[3][2] == 1


def goal_message(s):
    return "You've got all eight straight. Great!"


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
try:
    import sys

    init_state_string = sys.argv[2]
    print("Initial state as given on the command line: " + init_state_string)
    init_state_list = eval(init_state_string)
except:
    init_state_list = DEFAULT_INITIAL_STATE
    print("Using default initial state list: " + str(init_state_list))
    print(" (To use a specific initial state, enter it on the command line, e.g.,")
    print("python3 UCS.py EightPuzzle '[[3, 1, 2], [0, 4, 5], [6, 7, 8]]'")

CREATE_INITIAL_STATE = lambda: State(init_state_list)
# </INITIAL_STATE>

# <OPERATORS>
directions = ['N', 'E', 'W', 'S']
piece = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
possible_moves = [(1,'N'), (2,'N'), (3,'N'), (4,'N'), (5,'N'), (6,'N'), (7,'N'), (8,'N'), (9,'N'), (10,'N'),
                  (1,'E'), (2,'E'), (3,'E'), (4,'E'), (5,'E'), (6,'E'), (7,'E'), (8,'E'), (9,'E'), (10,'E'),
                  (1,'W'), (2,'W'), (3,'W'), (4,'W'), (5,'W'), (6,'W'), (7,'W'), (8,'W'), (9,'W'), (10,'W'),
                  (1,'S'), (2,'S'), (3,'S'), (4,'S'), (5,'S'), (6,'S'), (7,'S'), (8,'S'), (9,'S'), (10,'S')]
OPERATORS = [Operator("Move " + str(p) + " " + str(dir) + " into the void",
                      lambda s, p1 = p, dir1 = dir: s.can_move(p1,dir1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s, p1 = p, dir1 = dir: s.move(p1,dir1))
             for (p, dir) in possible_moves]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

