'''zl58_TTS.py
A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''
WHITE = 'W'
BLACK = 'B'
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
evalN = 0
states_expanded  = 0
ab_cutoffs = 0
whose_turn = ''
BETA = float('inf')
ALPHA = BETA * -1
NAME = ''
UT = 0
from TTS_State import TTS_State
import time
import math


#USE_CUSTOM_STATIC_EVAL_FUNCTION = True
USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
  def static_eval(self):
    global evalN
    evalN = evalN + 1
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()
  def basic_static_eval(self):
    TWF = 0
    TBF = 0
    for row in range(len(self.board)):
        for column in range(len(self.board)):
            if row == 0:
                U = len(self.board) - 1;
                D = 1
            elif row == len(self.board) - 1:
                U = len(self.board) - 2
                D = 0
            else:
                U = row - 1
                D = row + 1
            if column == 0:
                L = len(self.board) - 1;
                R = 1
            elif column == len(self.board) - 1:
                L = len(self.board) - 2
                R = 0
            else:
                L = column - 1
                R = column + 1
            N = [U, column]
            S = [D, column]
            W = [row, L]
            E = [row, R]
            NW = [U,L]
            NE = [U,R]
            SW = [D,L]
            SE = [D,R]
            if self.board[row][column] == WHITE:
                if self.board[N[0]][N[1]] == " ": TWF = TWF + 1
                if self.board[S[0]][S[1]] == " ": TWF = TWF + 1
                if self.board[W[0]][W[1]] == " ": TWF = TWF + 1
                if self.board[E[0]][E[1]] == " ": TWF = TWF + 1
                if self.board[NW[0]][NW[1]] == " ": TWF = TWF + 1
                if self.board[NE[0]][NE[1]] == " ": TWF = TWF + 1
                if self.board[SW[0]][SW[1]] == " ": TWF = TWF + 1
                if self.board[SE[0]][SE[1]] == " ": TWF = TWF + 1
            elif self.board[row][column] == BLACK:
                if self.board[N[0]][N[1]] == " ": TBF = TBF + 1
                if self.board[S[0]][S[1]] == " ": TBF = TBF + 1
                if self.board[W[0]][W[1]] == " ": TBF = TBF + 1
                if self.board[E[0]][E[1]] == " ": TBF = TBF + 1
                if self.board[NW[0]][NW[1]] == " ": TBF = TBF + 1
                if self.board[NE[0]][NE[1]] == " ": TBF = TBF + 1
                if self.board[SW[0]][SW[1]] == " ": TBF = TBF + 1
                if self.board[SE[0]][SE[1]] == " ": TBF = TBF + 1
    return TWF - TBF
  def custom_static_eval(self):
      length = len(self.board)
      board = self.board
      TWF = 0
      TBF = 0
      side = WHITE
      other_side = BLACK
      for row in range(length):
          count_state = 'not counting'
          cur_row = board[row]
          col = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if col == 0:
                  L = length - 1;
                  R = 1
              elif col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = col - 1
                  R = col + 1
              if state == 'initial':
                  if board[row][col] == side and cur_row[L] == side:  # start eval row
                      col = L
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1
                  if cur_row[col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      col = R
                      level = 2
                  else:
                      count_state = 'counting'
                      if cur_row[L] == other_side or cur_row[L] == '-':
                          level = level - 1
                      if cur_row[R] == side:
                          level += 1
                      if cur_row[R] == other_side or cur_row[R] == '-':
                          level = level - 1
                      col = R
          TWF += score
      for col in range(length):
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if col == 0:
                  L = length - 1;
                  R = 1
              elif col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = col - 1
                  R = col + 1
              if state == 'initial':
                  if board[row][col] == side and board[U][col] == side:  # start eval row
                      row = U
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if  board[row][col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][col] == other_side or board[U][col] == '-':
                          level = level - 1
                      if board[D][col] == side:
                          level += 1
                      if board[D][col] == other_side or board[D][col] == '-':
                          level = level - 1
                      row = D

          TWF += score
      for col in range(length):
          cur_col = col
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if cur_col == 0:
                  L = length - 1;
                  R = 1
              elif cur_col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = cur_col - 1
                  R = cur_col + 1
              if state == 'initial':
                  if board[row][cur_col] == side and board[U][L] == side:  # start eval row
                      row = U
                      cur_col = L
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if board[row][cur_col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      cur_col = R
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][L] == other_side or board[U][L] == '-':
                          level = level - 1
                      if board[D][R] == side:
                          level += 1
                      if board[D][R] == other_side or board[D][R] == '-':
                          level = level - 1
                      row = D
                      cur_col = R

          TWF += score
      for col in range(length):
          cur_col = col
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if cur_col == 0:
                  L = length - 1;
                  R = 1
              elif cur_col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = cur_col - 1
                  R = cur_col + 1
              if state == 'initial':
                  if board[row][cur_col] == side and board[U][L] == side:  # start eval row
                      row = U
                      cur_col = R
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if board[row][cur_col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      cur_col = L
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][R] == other_side or board[U][R] == '-':
                          level = level - 1
                      if board[D][L] == side:
                          level += 1
                      if board[D][L] == other_side or board[D][L] == '-':
                          level = level - 1
                      row = D
                      cur_col = L

          TWF += score
      side = BLACK
      other_side = WHITE
      for row in range(length):
          count_state = 'not counting'
          cur_row = board[row]
          col = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if col == 0:
                  L = length - 1;
                  R = 1
              elif col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = col - 1
                  R = col + 1
              if state == 'initial':
                  if board[row][col] == side and cur_row[L] == side:  # start eval row
                      col = L
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1
                  if cur_row[col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      col = R
                      level = 2
                  else:
                      count_state = 'counting'
                      if cur_row[L] == other_side or cur_row[L] == '-':
                          level = level - 1
                      if cur_row[R] == side:
                          level += 1
                      if cur_row[R] == other_side or cur_row[R] == '-':
                          level = level - 1
                      col = R
          TBF += score
      for col in range(length):
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if col == 0:
                  L = length - 1;
                  R = 1
              elif col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = col - 1
                  R = col + 1
              if state == 'initial':
                  if board[row][col] == side and board[U][col] == side:  # start eval row
                      row = U
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if  board[row][col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][col] == other_side or board[U][col] == '-':
                          level = level - 1
                      if board[D][col] == side:
                          level += 1
                      if board[D][col] == other_side or board[D][col] == '-':
                          level = level - 1
                      row = D
          TBF += score
      for col in range(length):
          cur_col = col
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if cur_col == 0:
                  L = length - 1;
                  R = 1
              elif cur_col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = cur_col - 1
                  R = cur_col + 1
              if state == 'initial':
                  if board[row][cur_col] == side and board[U][L] == side:  # start eval row
                      row = U
                      cur_col = L
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if board[row][cur_col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      cur_col = R
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][L] == other_side or board[U][L] == '-':
                          level = level - 1
                      if board[D][R] == side:
                          level += 1
                      if board[D][R] == other_side or board[D][R] == '-':
                          level = level - 1
                      row = D
                      cur_col = R

          TBF += score
      for col in range(length):
          cur_col = col
          count_state = 'not counting'
          row = 0
          count = 0
          state = 'initial'
          score = 0
          level = 2
          while count <= length:

              if row == 0:
                  U = length - 1;
                  D = 1
              elif row == length - 1:
                  U = length - 2
                  D = 0
              else:
                  U = row - 1
                  D = row + 1
              if cur_col == 0:
                  L = length - 1;
                  R = 1
              elif cur_col == length - 1:
                  L = length - 2
                  R = 0
              else:
                  L = cur_col - 1
                  R = cur_col + 1
              if state == 'initial':
                  if board[row][cur_col] == side and board[U][L] == side:  # start eval row
                      row = U
                      cur_col = R
                      count += 1
                      score = math.pow(2, count)
                  else:
                      state = 'begin'
                      count = 0
                      score = 0
              elif state == 'begin':
                  count += 1

                  if board[row][cur_col] != side:
                      if count_state == 'counting':
                          count_state = 'not counting'
                          score += math.pow(2, level)
                      row = D
                      cur_col = L
                      level = 2
                  else:
                      count_state = 'counting'
                      if board[U][R] == other_side or board[U][R] == '-':
                          level = level - 1
                      if board[D][L] == side:
                          level += 1
                      if board[D][L] == other_side or self.board[D][L] == '-':
                          level = level - 1
                      row = D
                      cur_col = L

          TBF += score
      return TWF - TBF



  def _find_next_vacancy(b):
      for i in range(len(b)):
          for j in range(len(b[0])):
              if b[i][j] == ' ': return (i, j)
      return False

  def _find_vacancy(self):
      vacant_spots = []
      for i in range(len(self.board)):
          for j in range(len(self.board[0])):
              if self.board[i][j] == ' ': vacant_spots.append((i, j))
      return vacant_spots


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
  new = MY_TTS_State(current_state.board, current_state.whose_turn)
  result = search(new,0,max_ply,alpha_beta, time.perf_counter(),2, ALPHA,BETA,new._find_vacancy(), use_custom_static_eval_function)
  DATA = {}
  DATA['CURRENT_STATE_STATIC_VAL'] = result['current_state_static_val']
  DATA['N_STATES_EXPANDED'] = result['n_states_expanded']
  DATA['N_STATIC_EVALS'] = result['n_static_evals_performed']
  DATA['N_CUTOFFS'] = result['n_ab_cutoffs']

  # STUDENTS: You may create the rest of the body of this function here.

  # Actually return all results...
  return(DATA)

def take_turn(current_state, opponents_utterance, time_limit=3):
    global UT

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.

    # Place a new tile
    if len(new_state._find_vacancy())==0: return [[False, current_state], "I don't have any moves!"]

    # Construct a representation of the move that goes from the
    # currentState to the newState.

    move = search(new_state, 0, 3, True, time.perf_counter(), time_limit, ALPHA, BETA, new_state._find_vacancy(), USE_CUSTOM_STATIC_EVAL_FUNCTION )["best_move"]
    # Make up a new remark

    new_utterance = "How about this"
    newboard = current_state.board
    new_who = BLACK
    if whose_turn == BLACK: new_who = WHITE
    newboard[move[0]][move[1]] = current_state.whose_turn
    utterances = [
        'How about this',
        'I AM VERY GOOD AT IT',
        'I am thinking...',
        'It is interesting',
        'it is too hard for me',
        'It can\'t be...',
        'It looks like I am winiing',
        'HAhaaaa',
        'hurry up',
        'I will beat you',
        'I feel board'
    ]
    UT += 1
    if UT >= 11:
        UT = 0

    new_utterance = utterances[UT]

    return [[move, MY_TTS_State(newboard, new_who)], new_utterance]

def search(current_state, max_depth, max_ply, alpha_beta, start_time, time_limit, alpha, beta, passed_spots,use_custom_static_eval_function):
    global states_expanded, ALPHA, BETA, ab_cutoffs,USE_CUSTOM_STATIC_EVAL_FUNCTION
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    curr_static_eval = current_state.static_eval()
    who = current_state.whose_turn
    curr_spots = passed_spots.copy()
    states_expanded += 1
    if max_depth > max_ply or len(curr_spots) == 0 or time.perf_counter() - start_time > 0.85 * time_limit:
        return {
            'current_state_static_val': curr_static_eval,
            'n_states_expanded': states_expanded,
            'n_static_evals_performed': evalN,
            'n_ab_cutoffs': ab_cutoffs,
            'best_move': None
        }
    board = current_state.board
    cur_location = curr_spots[0]
    new_spots = curr_spots.copy()
    new_spots.remove(cur_location)
    new_who = BLACK
    if who == BLACK: new_who = WHITE
    board[cur_location[0]][cur_location[1]] = who
    nextState = MY_TTS_State(board, new_who)

    bestS = search(nextState, max_depth + 1, max_ply, alpha_beta, start_time, time_limit, alpha, beta, new_spots, use_custom_static_eval_function)
    curr_static_eval = bestS['current_state_static_val']
    best_move = cur_location
    board[cur_location[0]][cur_location[1]] = ' '
    if who == WHITE and alpha < curr_static_eval :
        alpha = curr_static_eval
    elif who == BLACK and  beta > curr_static_eval :
        beta = curr_static_eval
    for tile in new_spots:
        if alpha_beta and beta <= alpha:
            ab_cutoffs += 1
            break

        board[tile[0]][tile[1]] = who
        nextState = MY_TTS_State(board, new_who)
        board[tile[0]][tile[1]] = ' '
        new_spot = curr_spots.copy()
        new_spot.remove(tile)
        nextS = search(nextState, max_depth + 1, max_ply, alpha_beta, start_time, time_limit, alpha, beta, new_spot, use_custom_static_eval_function)
        if who == WHITE:
            if alpha < nextS['current_state_static_val']:
                alpha = curr_static_eval
            if nextS['current_state_static_val'] > bestS['current_state_static_val']:
                best_move = tile
                curr_static_eval = nextS['current_state_static_val']
                bestS = nextS
        if who == BLACK:
            if beta > nextS['current_state_static_val']:
                beta = curr_static_eval
            if nextS['current_state_static_val'] < bestS['current_state_static_val']:
                best_move = tile
                curr_static_eval = nextS['current_state_static_val']
                bestS = nextS
    #print(best_move)
    return {
        'current_state_static_val':current_state.static_eval(),
        'n_states_expanded': states_expanded,
        'n_static_evals_performed': evalN,
        'n_ab_cutoffs': ab_cutoffs,
        'best_move': best_move
    }



def moniker():
    return "Eric" # Return your agent's short nickname here.
def who_am_i():
    return "My name is " + " Eric" + ", created by Zhiyao Li, " \
                                        "I consider myself to be a game master."


def get_ready(initial_state, k, what_side_i_play, player2Nickname):
    global INITIAL_STATE, K, whose_turn, NAME,USE_CUSTOM_STATIC_EVAL_FUNCTION
    global evalN,states_expanded, ab_cutoffs
    evalN = 0
    states_expanded = 0
    ab_cutoffs = 0

    INITIAL_STATE = initial_state
    K = k
    whose_turn = what_side_i_play
    NAME = player2Nickname
    initial_state.__class__ = MY_TTS_State
    USE_CUSTOM_STATIC_EVAL_FUNCTION = True
    return "OK"

GAME_TYPE =  "Gold Rush"




