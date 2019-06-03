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
from random import randint
import TTS_win_tester
import time

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
ALPHA_BETA = q
STATE={}
zobristnum = []
side = None
opponent = None
K = 0
row = 0
col = 0
n_states_expanded = 0
n_static_evals = 0
n_cutoffs = 0
best = None


class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
          return self.custom_static_eval()
        else:
          return self.basic_static_eval()

    def basic_static_eval(self):
        global row,col
        board = self.board
        return step_to_win(board) - step_to_lose(board)

    def custom_static_eval(self):
        global row, col
        TWF = 0
        TBF = 0
        board = self.board
        score = step_to_win(board) - step_to_lose(board)
        return score

    def move(self, step):
        s2 = self.copy()
        move = step
        s2.board[move[0]][move[1]] = s2.whose_turn
        if self.whose_turn == 'W':
            s2.whose_turn = 'B'
        else:
            s2.whose_turn = 'W'
        s2.__class__ = MY_TTS_State
        return s2

    def __hash__(self):
        return zhash(TTS_State.board)


def get_neighbor(board,i,j):
    score = 0
    total_row = len(board)
    total_col = len(board[0])
    # s
    if board[(i + 1) % total_row][j] == ' ':
        score = score + 1
    # n
    if board[(total_row + i - 1) % total_row][j] == ' ':
        score = score + 1
    # e
    if board[i][(j + 1) % total_col] == ' ':
        score = score + 1
    # w
    if board[i][(total_col + j - 1) % total_col] == ' ':
        score = score + 1
    # se
    if board[(i + 1) % total_row][(j + 1) % total_col] == ' ':
        score = score + 1
    # sw
    if board[(i + 1) % total_row][(total_col + j - 1) % total_col] == ' ':
        score = score + 1
    # nw
    if board[(total_row + i - 1) % total_row][(total_col + j - 1) % total_col] == ' ':
        score = score + 1
    # ne
    if board[(total_row + i - 1) % total_row][(j + 1) % total_col] == ' ':
        score = score + 1
    return score


def get_neighbors(board,i,j,who,dir):
    score = 0
    if who == 'W':opp = 'B'
    else: opp = 'W'
    neighborhoods = neighborhood(board,i,j,1)
    block = neighborhoods[dir]
    if block == who:
        for k in range(2,K+1):
            if neighborhood(board, i, j, k)[dir] == who:
                score = score + K + k^2
            elif neighborhood(board, i, j, k)[dir] == opp:
                score = score + K - k
            else:
                break
    elif block == opp:
        for k in range(2,K+1):
            if neighborhood(board, i, j, k)[dir] == opp:
                score = score + K + k ^ 2
            elif neighborhood(board, i, j, k)[dir] == who:
                score = score + K - k
            else:
                break
    elif block == ' ':
        score = score
    else:
        score = score - K
    return score


def step_to_win(board):
    best_step = 0
    row = len(board)
    col = len(board[0])
    for j in range(0, col):
        for i in range(0, row):
            block = board[i][j]
            if block == side:
                steps = line_up(board,i,j,block)
                if best_step < steps:
                    best_step = steps
    return best_step


def step_to_lose(board):
    if side == 'W':
        opp = 'B'
    else:
        opp = 'W'
    best_step = 0
    row = len(board)
    col = len(board[0])
    for j in range(0, col):
        for i in range(0, row):
            block = board[i][j]
            if block == opp:
                steps = line_up(board, i, j, block)
                if best_step < steps:
                    best_step = steps
    return best_step


def line_up(board,i,j,who):
    blocked = False
    best_step = 0
    if who == 'W':opp = 'B'
    else: opp = 'W'
    for k in range(0, 8):
        step = 0
        for l in range(1,K):
            nei = neighborhood(board, i, j, l)[k]
            if nei == who and not blocked:
                step = step + 1
            elif nei == opp or nei == '-':
                step = step / 2
                break
        if best_step < step:
            best_step = step
    return best_step


def neighborhood(board,i,j,dis):
    total_row = len(board)
    total_col = len(board[0])
    return [board[(i + dis) % total_row][j], board[(total_row + i - dis) % total_row][j],
                    board[i][(j + dis) % total_col], board[i][(total_col + j - dis) % total_col],
                    board[(i + dis) % total_row][(j + dis) % total_col], board[(i + dis) % total_row][(total_col + j - dis) % total_col],
                    board[(total_row + i - dis) % total_row][(total_col + j - dis) % total_col],
                    board[(total_row + i - dis) % total_row][(j + dis) % total_col]]

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)


def parameterized_minimax(
       current_state=None,
       max_ply=2,
       alpha_beta=False,
       use_custom_static_eval_function=False):

    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    global USE_CUSTOM_STATIC_EVAL_FUNCTION, ALPHA_BETA, n_states_expanded, n_static_evals, n_cutoffs
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    ALPHA_BETA = alpha_beta
    current_state.__class__ = MY_TTS_State
    start = time.time()
    current_state_static_eval = current_state.static_eval
    STATE[zhash(current_state.board)] = current_state_static_eval
    n_states_expanded = 0
    n_static_evals = 0
    n_cutoffs = 0
    mini_max(current_state, max_ply, start, 1,float('-inf'),float('inf'))

    # STUDENTS: You may create the rest of the body of this function here.

    # Actually return all results...
    DATA = {}
    DATA['CURRENT_STATE_STATIC_VAL'] = current_state_static_eval
    DATA['N_STATES_EXPANDED'] = n_states_expanded
    DATA['N_STATIC_EVALS'] = n_static_evals
    DATA['N_CUTOFFS'] = n_cutoffs
    return DATA


def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    # ew_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    # who = current_state.whose_turn
    # new_who = 'B'
    # if who=='B': new_who = 'W'
    # new_state.whose_turn = new_who
    
    # Place a new tile
    # location = _find_next_vacancy(new_state.board)
    # if location==False: return [[False, current_state], "I don't have any moves!"]
    # new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # move = location

    # Make up a new remark
    # new_utterance = "I'll think harder in some future game. Here's my move"
    # current_state.__class__ = MY_TTS_State
    start = time.time()
    out_of_time = time_limit / 10
    depth = 1
    pair = [0,0]
    while time.time() - start + out_of_time < time_limit and depth < K:
        last_time = time.time()
        pair = iterative_deepening(current_state,depth,start,time_limit)
        depth += 1
        this_time = time.time()
        if this_time - last_time > out_of_time:
            out_of_time = this_time - last_time
    return [pair, respond(current_state)]


def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False


def moniker():
    return "Daaddy" # Return your agent's short nickname here.


def who_am_i():
    return """My name is BIBIBABIBO, created by Keyi Zhong. I am eager in lining up."""


def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global zobristnum ,side,K,row,col,opponent
    side = who_i_play
    if side == 'B':
        opponent = 'W'
    else:
        opponent = 'B'
    K = k

    board = initial_state.board
    row = len(board)
    col = len(board[0])
    S = row * col
    P = 2
    zobristnum = [[0]*P for i in range(S)]
    for i in range(S):
        for j in range(P):
            zobristnum[i][j] = randint(0,4294967296)
    return "OK"


def mini_max(current_state,ply,start,time_limit,alpha,beta):
    global STATE, n_states_expanded, n_static_evals, n_cutoffs
    if ply == 0 or not _find_next_vacancy(current_state.board):
        hashnum = zhash(current_state.board)
        if hashnum in STATE:
            return STATE[hashnum]
        else:
            evals = current_state.static_eval()
            STATE[hashnum] = evals
            n_static_evals += 1
            return evals
    if current_state.whose_turn == 'W':
        value = float("-inf")
    else:
        value = float("inf")
    possible = possible_move(current_state)
    n_states_expanded += 1
    for step in possible:
        out_of_time = time_limit / 10
        if time.time() - start + out_of_time < time_limit:
            new_state = current_state.move(step)
            if TTS_win_tester.get_win(new_state,step,K) != "No win":
                if new_state.whose_turn == side:
                    return float("-inf")
                else:
                    return float("inf")
            new_evals = mini_max(new_state, ply - 1, start, time_limit,alpha,beta)
            if current_state.whose_turn == 'W' and new_evals > value:
                value = new_evals
                alpha = max(value,alpha)
                if ALPHA_BETA and alpha >= beta:
                    n_cutoffs += 1
                    break
                return alpha
            elif current_state.whose_turn == 'B' and new_evals < value:
                value = new_evals
                beta = min(value, beta)
                if ALPHA_BETA and alpha >= beta:
                    n_cutoffs += 1
                    break
                return beta
    return value


def iterative_deepening(current_state, ply, start, time_limit):
    depth = 0
    alpha = float("-inf")
    beta = float("inf")
    current_state.__class__ = MY_TTS_State
    possible = possible_move(current_state)
    while depth < ply:
        global best
        for step in possible:
            new_state = current_state.move(step)
            if TTS_win_tester.get_win(new_state, step, K) != "No win":
                return [step, new_state]
            new_evals = mini_max(new_state, depth, start, time_limit,alpha,beta)
            if current_state.whose_turn == 'W' and new_evals > alpha:
                alpha = new_evals
                best = [step, new_state]
            elif current_state.whose_turn == 'B' and new_evals < beta:
                beta = new_evals
                best = [step, new_state]
        depth += 1
    return best


def zhash(board):
    val = 0
    row = len(board)
    col = len(board[0])
    for i in range(0, row):
        for j in range(0,col):
            piece = None
            if board[i][j] == 'B':
                piece = 0
            if board[i][j] == 'W':
                piece = 1
            if piece is not None:
                val ^= zobristnum[i][piece]
    return val


def possible_move(current_state):
    board = current_state.board
    move = []
    # turn = current_state.whose_turn
    # new_turn = 'W'
    # if turn == 'W': new_turn = 'B'
    row = len(board)
    col = len(board[0])
    for j in range(0, col):
        for i in range(0, row):
            if board[i][j] == ' ':
                # new_state = MY_TTS_State(current_state.board, new_turn)
                # new_state.board[i][j] = turn
                # new_state.move = (i, j)
                move.append([i,j])
    return move


def static_eval(state):
    return state.static_eval()


def respond(state):
    eval = state.static_eval()
    if eval > mini_max(state,1,time.time(),10,float('-inf'),float('inf')):
        if len(possible_move(state)) < 2:
            return 'It seems you are losing'
        if len(possible_move(state)) < 3:
            return 'you better watch out for this'
        if _find_next_vacancy(state.board) == [0, 0] or [0, 1] or [1, 0]:
            return 'Keep eye on left corner'
        if _find_next_vacancy(state.board) == [1, 1] or [2, 2] or [3, 3]:
            return 'Why wouldnt I try diagonal lol'
    elif eval < mini_max(state,1,time.time(),10,float('-inf'),float('inf')):
        if len(possible_move(state)) < 2:
            return 'Thats a good one.'
        if len(possible_move(state)) < 3:
            return 'You know you can keep it, but I wont let you'
        if _find_next_vacancy(state.board) == [0, 0] or [0, 1] or [1, 0]:
            return 'You missed it'
        if _find_next_vacancy(state.board) == [1, 1] or [2, 2] or [3, 3]:
            return 'Check out my move you will be surprised'
    else:
        if state.whose_turn == 'B':
            return 'Give it up!'
    return "Tie up? No way!"
