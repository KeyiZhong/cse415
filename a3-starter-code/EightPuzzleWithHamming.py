'''
EightPuzzleWithHamming.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
'''

from EightPuzzle import *

CORRECT = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]

def h(s):
  '''Return the number of tiles that out of place'''
  list = s.b
  count = 0
  for i in range(1,9):
      row = int(i/3)
      col = i%3
      if CORRECT[row][col] != list[row][col]:
          count = count + 1
  return count

# A simple test:
# print(h([[3,0,1],[6,4,2],[7,8,5]]))
