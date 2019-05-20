'''keyi_BC_Player.py.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
BLACK = 0
WHITE = 1

PIECE_VALUES = {
    'p':lambda s :  1,
    'c':lambda s :  2,
    'l':lambda s :  2,
    'i':lambda s :  2,
    'w':lambda s :  2,
    'k':lambda s :  100,
    'f':lambda s :  2,
    '-':lambda s:  0
}

def parameterized_minimax(currentState, alphaBeta=False, ply=3,\
    useBasicStaticEval=True, useZobristHashing=False):
  '''Implement this testing function for your agent's basic
  capabilities here.'''

  pass


def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((2, 2), (2, 3))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]


def nickname():
    return "Newman"


def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."


def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    pass


def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    pass


def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''

    pass


def getKing(state):

    pass


def possibleMOve(state):

    pass

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf
  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

valid_coords = list(itertools.product(range(8), range(8))) # board dim is 8
OPERATORS = [
    Operator("move from %s to %s", lambda s, start=start, end=end: can_move(s, start, end), lambda s, start=start, end=end: move(s, start, end))
    for start,end, in itertools.product(valid_coords, valid_coords)
  ]

def check_op(op, state):
    if op.precond(state[1]):
        new = op.state_transf(state[1])
        MoveTree[zhash(state[1])].append([staticEval(state[1]),new])


def minimax(state,depth, whose=None, alphabeta=[-1*float('inf'), float('inf')]):
    alphabeta = alphabeta[:]
    if depth < 1: # this is a leaf node
        cost = staticEval(state[1])
        state[0] = cost
        return cost
    else: # this is not a leaf node
        if zhash(state[1]) not in MoveTree:
            for x, row in enumerate(state[1].board):
                for y, col in enumerate(row):
                    piece = CODE_TO_INIT[col]

                    for op in OPERATORS:
                        check_op(op,state)
        if whose == WHITE: # Max move
            v = -1*float('inf')
            for ci,child in enumerate(sorted(MoveTree[zhash(state[1])], key=lambda x: x[0], reverse=True)):
                sub_cost = minimax(child, depth-1, whose=BLACK, alphabeta=alphabeta)
                v = max(v, sub_cost)
                MoveTree[zhash(state[1])][ci][0] = v
                alpha = max(alphabeta[0], v)
                alphabeta[0] = alpha
                if alphabeta[1] <= alphabeta[0]:
                    break
            return v
        else: # Min move
            v = float('inf')
            for ci,child in enumerate(sorted(MoveTree[zhash(state[1])], key=lambda x: x[0], reverse=False)):
                sub_cost = minimax(child, depth-1, whose=WHITE, alphabeta=alphabeta)
                v = min(v, sub_cost)
                MoveTree[zhash(state[1])][ci][0] = v
                beta = min(alphabeta[1], v)
                alphabeta[1] = beta
                if alphabeta[1] <= alphabeta[0]:
                    break
            return v
