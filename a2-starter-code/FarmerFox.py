'''FarmerFox.py
("Farmer Fox Chicken and Grain" problem)
'''
# <METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer Fox Chicken and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Keyi Zhong']
PROBLEM_CREATION_DATE = "15-APR-2019"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Missionaries and Cannibals"</b> problem is a traditional puzzle
in which the player starts off with three missionaries and three cannibals
on the left bank of a river.  The object is to execute a sequence of legal
moves that transfers them all to the right bank of the river.  In this
version, there is a boat that can carry at most three people, and one of
them must be a missionary to steer the boat.  It is forbidden to ever
have one or two missionaries outnumbered by cannibals, either on the
left bank, right bank, or in the boat.  In the formulation presented
here, the computer will not let you make a move to such a forbidden situation, and it
will only show you moves that could be executed "safely."
'''
#</METADATA>

#<COMMON_DATA>

#</COMMON_DATA>

#<COMMON_CODE>
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.
Fa = 0
Fo = 1
C = 2
G = 3
q = ['F','f','c','g']


class State():

  def __init__(self, d=None):
    if d == None:
      d = [LEFT, LEFT, LEFT, LEFT]
    left = 'Ffcg'
    right = ''
    self.d = d
    self.right = right
    self.left = left

  def __eq__(self,s2):
    if self.d != s2.d: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = "\n Left bank: " + self.left + "\n"
    txt += " Right bank: " + self.right + "\n"
    side = 'left'
    if self.d[0] == 1:
      side = 'right'
    txt += " boat is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State(None)
    for i in range(4 ):
      news.d[i] = self.d[i]
    return news

  # move is a string in 'F' 'f' 'c' 'g'
  def can_move(self, move):
    '''Tests whether it's legal to move the boat with this movement'''
    news = self.copy()
    p = news.d
    side = news.d[0]  # Where the boat is.
    index = q.index(move)
    if p[index] != side:
      return False
    p[index] = 1 - p[index]
    if index != 0:
      p[0] = 1 - p[0]
    news.left = ''
    news.right = ''
    for i in range(4):
      if p[i] == LEFT:
        news.left += q[i]
      else:
        news.right += q[i]
    not_legal = ['fc','cg']
    return (news.left not in not_legal) and (news.right not in not_legal)


  def move(self,move):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
    news = self.copy()      # start with a deep copy.
    p = news.d         # get the array of arrays of people.
    index = q.index(move)
    p[index] = 1 - p[index]
    if index != 0:
      p[0] = 1 - p[0]
    news.left = ''
    news.right = ''
    for i in range(4):
      if p[i] == LEFT:
        news.left += q[i]
      else:
        news.right += q[i]
    return news

def goal_test(s):
  '''If Ffgc is on the right then it is a goal state'''
  p = s.d
  return (p == [RIGHT, RIGHT, RIGHT, RIGHT])

def goal_message(s):
  return "Congratulations on successfully guiding the Farmer Fox Chicken and Grain across the river!"

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
CREATE_INITIAL_STATE = lambda: State(d=[LEFT,LEFT,LEFT,LEFT])
# </INITIAL_STATE>


# <OPERATORS>
Ffgc_combinations = ['Farmer','fox','chicken','grain']

OPERATORS = [Operator(
  "Cross the river with " + move,
  lambda s, move1 = move[0]: s.can_move(move1),
  lambda s, move1 = move[0]: s.move(move1))
  for move in Ffgc_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
