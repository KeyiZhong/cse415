'''
EightPuzzleWithHamming.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
'''

from klotski import *


def h(s):
  '''Return the number of tiles that out of place'''
  list = s.b
  count = 0
  for i in range(5):
      for j in range(4):
          if checkaround(list,i,j):
              count += 1
  return count

def checkaround(b, i, j):
    try:
        if b[i - 1][j - 1] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i + 1][j - 1] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i - 1][j + 1] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i][j - 1] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i][j + 1] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i - 1][j] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i + 1][j] == 1:
            return True
    except IndexError:
        pass
    try:
        if b[i + 1][j + 1] == 1:
            return True
    except IndexError:
        pass


# A simple test:
# print(h([[3,0,1],[6,4,2],[7,8,5]]))
