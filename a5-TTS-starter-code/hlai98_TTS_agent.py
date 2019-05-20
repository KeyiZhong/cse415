'''PlayerSkeleton.py
A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''

from TTS_State import TTS_State
import time

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

N_CUTOFFS = 0
N_STATIC_EVALS = 0

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        TWF = 0
        TBF = 0
        board = self.board
        mRows = len(board)
        mColumns = len(board[0])
        for i in range(mColumns):
            for j in range(mRows):
                if board[i][j] == "W":
                    TWF += self.basic_static_helper(i, j)
                if board[i][j] == "B":
                    TBF += self.basic_static_helper(i, j)
        scores = TWF - TBF
        return scores

    def basic_static_helper(self, i, j):
        board = self.board
        score = 0
        for a in (-1,0,1):
            for b in (-1,0,1):
                if board[i+a][j+b] == " ":
                    score+=1
        return score

    def custom_static_eval(self):
        scores = 0
        return scores

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

def parameterized_minimax(current_state=None, max_ply=2, use_alpha_beta=False, use_basic_static_eval=True):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    #    global INITIAL_STATE, my_side, K, opponent, op_side

    DATA = {}
    DATA['CURRENT_STATE_STATIC_VAL'] = -1000.0
    #DATA['N_STATES_EXPANDED'] = 0
    #DATA['N_STATIC_EVALS'] = 0
    #DATA['N_CUTOFFS'] = 0

    # STUDENTS: You may create the rest of the body of this function here.
    global BASIC
    BASIC = False
    if use_basic_static_eval:
        BASIC = True
    current_state.__class__ = MY_TTS_State
    if use_basic_static_eval:
        DATA['CURRENT_STATE_STATIC_VAL'] = current_state.basic_static_eval()
    else:
        DATA['CURRENT_STATE_STATIC_VAL'] = current_state.custom_static_eval()

    if use_alpha_beta:
        value = alpha_beta(my_side, current_state, max_ply, -100000, 100000)
    else:
        value = minimax_search(my_side, current_state, max_ply)
    USE_ITERATIVE_DEEPENING = False

        # Actually return all results...
    # return dict
    DATA['N_CUTOFFS'] = N_CUTOFFS
    DATA['N_STATIC_EVALS'] = N_STATIC_EVALS
    DATA['N_STATES_EXPANDED'] = N_STATES_EXPANDED
    return (DATA)

def alpha_beta(side, state, plyLeft, alpha, beta):
    global N_CUTOFFS, N_STATIC_EVALS, N_STATES_EXPANDED
    sign = 1
    if my_side == "B":
        sign = -1
    if plyLeft == 0 or _find_next_vacancy(state) == False:
        N_STATIC_EVALS += 1
        if BASIC:
            return (sign * state.basic_static_eval())
        return (sign * state.custom_static_eval())
    next = _find_next_vacancy(state)
    empty = []
    while next != False:
        empty.append(next)
        next = _find_next_vacancy(state)
    successors = []
    for s in empty:
        temp = state
        temp[s] = side
        successors.append(temp)
    for s in successors:
        N_STATES_EXPANDED += 1
        if side == my_side:
            value = -100000
            value = max(value, alpha_beta(player(side), s, plyLeft - 1, alpha, beta))
            alpha = max(alpha,value)
            if alpha >= beta:
                N_CUTOFFS += 1
                break
            return value
        elif side == op_side:
            value = 100000
            value = min(value, alpha_beta(player(side), s, plyLeft - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                N_CUTOFFS += 1
                break
    return value


def minimax_search(side, state, plyLeft):
    global N_STATIC_EVALS, N_STATES_EXPANDED
    sign = 1
    if my_side == "B":
        sign = -1
    if plyLeft == 0 or _find_next_vacancy(state) == False:
        N_STATIC_EVALS += 1
        if BASIC:
            return (sign * state.basic_static_eval())
        return (sign * state.custom_static_eval())
    next = _find_next_vacancy(state)
    empty = []
    while next != False:
        empty.append(next)
        next = _find_next_vacancy(state)
    successors =[]
    for s in empty:
        temp = state
        temp[s] = side
        successors.append(temp)
    if side == my_side:
        value = -100000
    else:
        value = 100000
    for s in successors:
        N_STATES_EXPANDED += 1
        newVal = minimax_search(player(side), s, plyLeft - 1)
        if (side == my_side and newVal > value) or (side == op_side and newVal < value):
            value = newVal
    return value


def player(current):
    if current == my_side:
        return op_side
    return my_side







def take_turn(current_state, opponents_utterance, time_limit=3):
    global start, TIME_LIMIT, USE_ITERATIVE_DEEPENING
    start = time.time()
    TIME_LIMIT = time_limit

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'
    new_state.whose_turn = new_who




    # Place a new tile
    location = _find_next_vacancy(new_state.board)

    while start <= TIME_LIMIT:
        if USE_ITERATIVE_DEEPENING:
            location = iterative_deepening(current_state)
        else:
            location = minimax_search(my_side, current_state, len(current_state.board))


    if location == False: return [[False, current_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = "I'll think harder in some future game. Here's my move"

    return [[move, new_state], new_utterance]


def iterative_deepening(state):
    global MAX_DEPTH
    location = False
    best_score = -100000

    next = _find_next_vacancy(state)
    empty = []
    while next != False:
        empty.append(next)
        next = _find_next_vacancy(state)


    for ply in range(1, len(empty) + 1):
        global TIMED
        end = time.time()
        if TIMED and end - start > TIME_LIMIT - 0.005:
            break
        new_best = minimax_search(my_side, state, ply)
        MAX_DEPTH = ply
        if new_best > best_score:
            #location = new_location
            best_score = new_best
        return location

def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': return (i, j)
    return False


def moniker():
    return "Aggie"  # Return your agent's short nickname here.


def who_am_i():
    return """My name is Aggie Smarty, created by Yvonne Lai (hlai98).
I consider myself to be the smartest player."""


def get_ready(initial_state, k, what_side_i_play, opponent_moniker):
    global INITIAL_STATE, my_side, K, opponent, op_side
    K = k
    my_side = what_side_i_play
    op_side = "W"
    if my_side == "W":
        op_side = "B"
    INITIAL_STATE = initial_state
    opponent = opponent_moniker
    # do any prep, like eval pre-calculation, here.
    return "OK"
