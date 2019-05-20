from TTS_State import TTS_State
from TTS_win_tester import get_win as goal_test
import time
from random import randint
from functools import reduce

class My_Priority_Queue:
    def __init__(self):
        self.q = []     # Actual data goes in a list.

    def __contains__(self, elt):
        """If there is a (state, priority) pair on the list where
        state==element (elt), then return True."""
        for pair in self.q:
            if pair[0] == elt:
                return True
        return False

    def delete_min(self):
        """Standatd priority-queue dequeing method."""
        if self.q == []:
            return []  # Simpler than raising an exception.
        temp_min_pair = self.q[0]
        temp_min_value = temp_min_pair[1]
        temp_min_position = 0
        for j in range(1, len(self.q)):
            if self.q[j][1] < temp_min_value:
                temp_min_pair = self.q[j]
                temp_min_value = temp_min_pair[1]
                temp_min_position = j
        del self.q[temp_min_position]
        return temp_min_pair

    def insert(self, state, priority):
        """We do not keep the list sorted, in this implementation."""
        # print("calling insert with state, priority: ", state, priority)

        if self[state] != -1:
            print("Error: You're trying to insert an element into a "
                  "My_Priority_Queue instance,")
            print(" but there is already such an element in the queue.")
            return
        self.q.append((state, priority))

    def __len__(self):
        """We define length of the priority queue to be the
        length of its list."""
        return len(self.q)

    def __getitem__(self, state):
        """This method enables Pythons right-bracket syntax.
        Here, something like  priority_val = my_queue[state]
        becomes possible. Note that the syntax is actually used
        in the insert method above:  self[state] != -1  """
        for (S, P) in self.q:
            if S == state: return P
        return -1  # This value means not found.

    def __delitem__(self, state):
        """This method enables Python's del operator to delete
        items from the queue."""
        print("In MyPriorityQueue.__delitem__: state is: ", str(state))
        for count, (S, P) in enumerate(self.q):
            if S == state:
                del self.q[count]
                return

    def __str__(self):
        txt = "My_Priority_Queue: ["
        for (s, p) in self.q: txt += '(' + str(s) + ',' + str(p) + ') '
        txt += ']'
        return txt

    def delete_max(self):
        """Remove largest priority valued item."""
        if self.q == []:
            return []  # Simpler than raising an exception.
        temp_max_pair = self.q[0]
        temp_max_value = temp_max_pair[1]
        temp_max_position = 0
        for j in range(1, len(self.q)):
            if self.q[j][1] > temp_max_value:
                temp_max_pair = self.q[j]
                temp_max_value = temp_min_pair[1]
                temp_max_position = j
        del self.q[temp_max_position]
        return temp_max_pair

zobristnum = []

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
K = 2
OPPONENT = None
OPPONENT_COLOR = None
SIDE = None
current_turn = None
BOARD = None
EXPLORED_STATES = {}
max_depth_reached = 0
COUNTS = {}
n_states_expanded = 0
n_static_evals_performed = 0
n_ab_cutoffs = 0
default_moves = False
pruning = True
empty_tiles = None
time_buffer = 0.00
FIRST_MOVE = False
alpha = -100000
beta = 100000
last_count = None

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        global COUNTS
        COUNTS = {'W': [0 for n in range(K + 1)],
                  'B': [0 for n in range(K + 1)]}
        board = self.board
        board_transp = list(map(list, zip(*board)))
        rows = len(board)
        cols = len(board[0])
        W = 0
        B = 0
        for i in range(rows):
            for j in range(cols):
                # No connecting lines if the tile is forbidden
                if board[i][j] == '-':
                    continue
                # check East
                if board[i].count('W') == 2 or board[i].count('B') == 2:
                    nxt_k = board[i][j: j + K]
                    if len(nxt_k) < K:
                        nxt_k += board[i][:(j + K) % cols]
                    # check for no forbidden squares in nxt_k
                    if '-' not in nxt_k:
                        # check for only W or B squares in nxt_k
                        if nxt_k.count('B') == 2 or nxt_k.count('W') == 2:
                            if 'W' in nxt_k:
                                if 'B' not in nxt_k:
                                    COUNTS['W'][nxt_k.count('W')] += 1
                            elif 'B' in nxt_k:
                                COUNTS['B'][nxt_k.count('B')] += 1
                # check South
                if board_transp[j].count('W') == 2 or \
                        board_transp[j].count('B') == 2:
                    nxt_k = board_transp[j][i: i + K]
                    if len(nxt_k) < K:
                        nxt_k += board_transp[j][: (i + K) % rows]
                    if '-' not in nxt_k:
                        # check for only W or B squares in nxt_k
                        if nxt_k.count('B') == 2 or nxt_k.count('W') == 2:
                            if 'W' in nxt_k:
                                if 'B' not in nxt_k:
                                    COUNTS['W'][nxt_k.count('W')] += 1
                            elif 'B' in nxt_k:
                                COUNTS['B'][nxt_k.count('B')] += 1
                SE = [board[(i + n) % rows][(j + n) % cols] for n in
                      range(K)]
                NE = [board[(i - n) % rows][(j + n) % cols] for n in
                      range(K)]
                # check SE
                if '-' not in SE:
                    if SE.count('B') == 2 or SE.count('W') == 2:
                        if 'W' in SE and 'B' not in SE:
                            COUNTS['W'][SE.count('W')] += 1
                        elif 'B' in SE and 'W' not in SE:
                            COUNTS['B'][SE.count('B')] += 1
                # check NE
                if '-' not in NE:
                    if NE.count('B') == 2 or NE.count('W') == 2:
                        if 'W' in NE and 'B' not in NE:
                            COUNTS['W'][NE.count('W')] += 1
                        elif 'B' in NE and 'W' not in NE:
                            COUNTS['B'][NE.count('B')] += 1
        return COUNTS['W'][2] - COUNTS['B'][2]

    def custom_static_eval(self):
        global COUNTS
        COUNTS = self.count_state()
        for n in range(K):
            if COUNTS['B'][K] > 0:
                return -10000000000000000
            if COUNTS['W'][K] > 0:
                return 1000000000000000
        B = reduce(lambda x, y: x + y, [COUNTS['B'][i] * 10 ** i
                                        for i in range(K)])
        W = reduce(lambda x, y: x + y, [COUNTS['W'][i] * 10 ** i
                                        for i in range(K)])
        F = reduce(lambda x, y: x + y, [COUNTS['F'][i] * i
                                        for i in range(K)])
        if self.whose_turn == 'W':
            return W - B - F
        return W - B + F

    def count_state(self):
        COUNTS = {'W': [0 for n in range(K + 1)],
                  'B': [0 for n in range(K + 1)],
                  'F': [0 for n in range(K + 1)]}
        board = self.board
        board_transp = list(map(list, zip(*board)))
        rows = len(board)
        cols = len(board[0])
        for i in range(rows):
            for j in range(cols):
                # No connecting lines if the tile is forbidden
                if board[i][j] == '-':
                    continue
                # check East
                if 'W' or 'B' in board[i]:
                    nxt_k = board[i][j: j + K]
                    if len(nxt_k) < K:
                        nxt_k += board[i][:(j + K) % cols]
                    # check for no forbidden squares in nxt_k
                    if '-' not in nxt_k:
                        # check for only W or B squares in nxt_k
                        if 'W' in nxt_k:
                            if 'B' not in nxt_k:
                                COUNTS['W'][nxt_k.count('W')] += 1
                        elif 'B' in nxt_k:
                            COUNTS['B'][nxt_k.count('B')] += 1
                # check South
                if 'W' or 'B' in board_transp[j]:
                    nxt_k = board_transp[j][i: i + K]
                    if len(nxt_k) < K:
                        nxt_k += board_transp[j][: (i + K) % rows]
                    if '-' not in nxt_k:
                        # check for only W or B squares in nxt_k
                        if 'W' in nxt_k:
                            if 'B' not in nxt_k:
                                COUNTS['W'][nxt_k.count('W')] += 1
                        elif 'B' in nxt_k:
                            COUNTS['B'][nxt_k.count('B')] += 1
                SE = [board[(i + n) % rows][(j + n) % cols] for n in
                      range(K)]
                NE = [board[(i - n) % rows][(j + n) % cols] for n in
                      range(K)]
                # check SE
                if '-' not in SE:
                    if 'W' in SE and 'B' not in SE:
                        COUNTS['W'][SE.count('W')] += 1
                    elif 'B' in SE and 'W' not in SE:
                        COUNTS['B'][SE.count('B')] += 1
                # check NE
                if '-' not in NE:
                    if 'W' in NE and 'B' not in NE:
                        COUNTS['W'][NE.count('W')] += 1
                    elif 'B' in NE and 'W' not in NE:
                        COUNTS['B'][NE.count('B')] += 1
        return COUNTS

    def can_move(self, tile):
        if tile == False:
            return False
        i, j = tile
        return self.board[i][j] == ' '

    def move(self, tile):
        s2 = self.copy()
        i, j = tile
        s2.board[i][j] = s2.whose_turn
        if self.whose_turn =='W':
            s2.whose_turn = 'B'
        else:
            s2.whose_turn = 'W'
        s2.__class__ = MY_TTS_State
        return s2

    def __hash__(self):
        return zhash(self.board)


def take_turn(current_state, last_utterance, time_limit):
    """Searches the game state and returns the best play."""
    global EXPLORED_STATES, max_depth_reached, FIRST_MOVE
    start = time.time()
    current_state.__class__ = MY_TTS_State
    # Compute the new state for a move.
    # # Start by copying the current state.
    # new_state = MY_TTS_State(current_state.board)
    # # Fix up whose turn it will be.
    # who = current_state.whose_turn
    # new_who = 'B'
    # if who=='B': new_who = 'W'
    # new_state.whose_turn = new_who
    # Place a new tile
    depth = 0
    stop_time = time_limit - time_buffer
    while time.time() - start < time_limit:
        move, new_state = Depth_Limited_Search(current_state, depth + 1, start,
                                               stop_time)
    if move == False:
        return [[False, current_state], "Good game, looks like we tied!"]

    # Construct a representation of the move that goes from the
    # currentState to the newState.


    return [[move, new_state], utterances(current_state)]


def _find_next_vacancy(b):
    for i, row in enumerate(b):
        if ' ' in row:
            return (i, row.index(' '))
    return False

def who_am_i():
    return """My name is Dunkin, created by Michael Ruby, (UWNETID ruby7188).  
    I take advantage of the doughnut like shape of the board to connect my 
    pieces.  You better be on top of your game if you hope to beat me."""


def moniker():
    return 'Dunkin'


def get_ready(initial_state, k, who_i_play, player2Nickname):
    """Prepares the agemnt to play the game, assigning which side"""
    global K, OPPONENT, SIDE, current_turn, OPPONENT_COLOR, BOARD, OPPONENT, \
        zobristnum
    S = len(initial_state.board) * len(initial_state.board[0])
    P = 2
    zobristnum = [[0] * P for i in range(S)]
    for i in range(S):
        for j in range(P):
            zobristnum[i][j] = randint(0, 4294967296)
    if k > 2:
        K = k
    SIDE = who_i_play
    OPPONENT = player2Nickname
    BOARD = initial_state.board
    if SIDE == 'W':
        OPPONENT_COLOR = 'B'
    else:
        OPPONENT_COLOR = 'W'
    initial_state.__class__ = MY_TTS_State
    initial_eval = initial_state.static_eval()
    EXPLORED_STATES[initial_state] = initial_eval

    return "OK"

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

def parameterized_minimax(
        current_state=None,
        use_iterative_deepening_and_time = False,
        max_ply = 2,
        use_default_move_ordering = False,
        alpha_beta=False,
        time_limit=1.0,
        use_custom_static_eval_function=False):
    global n_states_expanded, n_static_evals_performed, \
        USE_CUSTOM_STATIC_EVAL_FUNCTION, default_moves, pruning, \
        max_depth_reached, n_ab_cutoffs, hard_ply_limit, n_states_expanded
    hard_ply_limit = True
    default_moves = use_default_move_ordering
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    pruning = alpha_beta
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    if current_state == None:
        raise ValueError("No State entered")
    start = time.time()
    current_state.__class__ = MY_TTS_State
    current_state_static_val = current_state.static_eval()
    EXPLORED_STATES[current_state] = current_state_static_val
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    n_ab_cutoffs = 0
    # STUDENTS: You may create the rest of the body of this function here.
    current_state.__class__ = MY_TTS_State
    if use_iterative_deepening_and_time:
        Depth_Limited_Search(current_state, max_ply, start, time_limit)
    else:
        minimax(current_state, max_ply, start, time_limit)
    # Prepare to return the results, don't change the order of the results
    results = []
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    # Actually return the list of all results...
    return (results)


def minimax(current_state, plyLeft, start, time_limit):
    """Uses alpha-beta pruning to find the optimal route."""
    global n_states_expanded, n_static_evals_performed, n_ab_cutoffs, \
        EXPLORED_STATES, alpha, beta, max_depth_reached
    if plyLeft == 0:
        if current_state in EXPLORED_STATES:
            return EXPLORED_STATES[current_state]
        else:
            val = current_state.static_eval()
            n_static_evals_performed += 1
            EXPLORED_STATES[current_state] = val
            return val
    if current_state.whose_turn == 'W':
        provisional = -100000
    else:
        provisional = 10000
    empty_tiles = open_spaces(current_state)
    if len(empty_tiles) == 0:
        if current_state in EXPLORED_STATES:
            return EXPLORED_STATES[current_state]
        val = current_state.static_eval()
        EXPLORED_STATES[current_state] = val
        return val
    n_states_expanded += 1
    alpha = -100000
    beta = 10000
    for tile in empty_tiles:
        if time.time() - start < time_limit:
            new_state = current_state.move(tile)
            if goal_test(new_state, tile, K) != "No win":
                if new_state in EXPLORED_STATES:
                    val = EXPLORED_STATES[new_state]
                else:
                    val = new_state.static_eval()
                    EXPLORED_STATES[new_state] = val
                return val
            newVal = minimax(new_state, plyLeft - 1, start, time_limit)
            max_depth_reached += 1
            if current_state.whose_turn == 'W' and newVal > provisional:
                provisional = newVal
                alpha = max(provisional, alpha)
                if pruning and alpha >= beta:
                    n_ab_cutoffs = n_ab_cutoffs + 1
                    break
                return alpha
            elif current_state.whose_turn == 'B' and newVal < provisional:
                provisional = newVal
                beta = min(provisional, beta)
                if pruning and alpha >= beta:
                    n_ab_cutoffs = n_ab_cutoffs + 1
                    break
                return beta
    return provisional


def Depth_Limited_Search(current_state, plyLimit, start, time_limit):
    """Finds the optimal route using IDDFS and minimax"""
    global EXPLORED_STATES, max_depth_reached, empty_tiles, n_ab_cutoffs, \
        alpha, beta
    alpha = -100000
    beta = 100000
    L = My_Priority_Queue()
    depth = 0
    MOVES = open_spaces(current_state)
    best_move = None
    if (time.time() - start) < time_limit:
        while plyLimit > depth:
            if not _find_next_vacancy(current_state.board):
                return [False, current_state]
            if default_moves:
                MOVES = open_spaces(current_state)
            for move in MOVES:
                new_state = current_state.move(move)
                if goal_test(new_state, move, K) != 'No win':
                    return [move, new_state]
                newVal = minimax(new_state, depth, start, time_limit)
                if current_state.whose_turn == 'W':
                    if newVal > alpha:
                        print(alpha)
                        print(newVal)
                        print(move)
                        alpha = newVal
                        best_move = [move, new_state]
                        if pruning and alpha >= beta:
                            n_ab_cutoffs = n_ab_cutoffs + 1
                elif current_state.whose_turn == 'B':
                    if newVal < beta:
                        beta = newVal
                        best_move = [move, new_state]
                        if pruning and alpha >= beta:
                            n_ab_cutoffs = n_ab_cutoffs + 1
                else:
                    L.insert(move, newVal)
            while L:
                if current_state.whose_turn == 'W':
                    MOVES.append(L.delete_max())
                else:
                    MOVES.append(L.delete_max())

            depth += 1
            max_depth_reached = max(depth, max_depth_reached)
    return best_move


def open_spaces(current_state):
    """Returns a list of all open spaces on the board"""
    return [(i, j) for j in range(len(current_state.board[0])) for i
            in range(len(current_state.board))
            if current_state.board[i][j] == ' ']


def zhash(board):
    """Returns a zogrist hash of the game board"""
    global zobristnum
    b = [tile for row in board for tile in row]
    val = 0
    for i in range(len(b)):
        piece = None
        if b[i] == 'B':
            piece = 0
        elif b[i] == 'W':
            piece = 1
        if piece is not None:
            val ^= zobristnum[i][piece]
    return val

def utterances(current_state):
    """Returns a phrase based on the current games state."""
    global last_count
    utterance = ''
    if last_count == None:
        utterance = 'Good luck you better make your moves count.'
    eval = current_state.static_eval()
    if SIDE == 'W':
        OTHER = 'B'
    else:
        OTHER = 'W'
    if COUNTS[SIDE][K - 1] > 0:
        if COUNTS[OTHER][K - 1] == 0:
            if COUNTS[SIDE][K - 1] > 1:
                utterance = "HAHA, the game is mine!, you will never be able " \
                            "to stop my victory."
            else:
                utterance = "You better play this carefully. I have a winning" \
                            " move"
        else:
            utterance = "You won't be so lucky next time..."
    elif COUNTS[SIDE][K - 2] > 0:
        if COUNTS[OTHER][K - 2] > 0:
            if COUNTS[SIDE][K - 2] - COUNTS[OTHER][K - 2] > 0:
                utterance = "I have a clear advantage now"
            elif COUNTS[SIDE][K - 2] - COUNTS[OTHER][K - 2] == 0:
                utterance = "This is a close Game"
            else:
                utterance = "You have, the advantage now, but you won't for " \
                            "long."
    else:
        if eval > 0:
            if SIDE == 'W':
                utterance = 'The outcome in uncertain but I have a clear ' \
                            'advantage according to my calculations.'
            else:
                utterance = 'You seem to have the advantage, you better play ' \
                            'carefully if you hope to keep it.'
        if eval == 0:
            utterance = 'Wow, this game is increadibly close.'
        if eval < 0:
            if SIDE == 'B':
                utterance = 'The outcome in uncertain but I have a clear ' \
                            'advantage according to my calculations.'
            else:
                utterance = 'You seem to have the advantage, you better play ' \
                            'carefully if you hope to keep it.'
    last_count = eval
    return OPPONENT + ', ' + utterance