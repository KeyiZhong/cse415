'''
EightPuzzleWithManhattan.py
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
      t_row=0
      t_col=0
      for j in range(3):
          try: t_col = list[j].index(i)
          except: continue
          else:t_row = j
      count = count + abs(row-t_row) + abs(col-t_col)
  return count

# A simple test:
# print(h([[3,0,1],[6,4,2],[7,8,5]]))
