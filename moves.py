from copy import deepcopy
from tkinter import *
from math import *
from time import *
from random import *
from game_canvas import *
from gui import *

SIZE = 8
WHITE = 0
BLACK = 1


def count_different(board, player):
  if player == BLACK:
    colour = "black"
    opponent = "white"
  else:
    colour = "white"
    opponent = "black"
  colour_num = 0
  opponent_num = 0
  for x in range(SIZE):
    for y in range(SIZE):
      if board[x][y] == colour:
        colour_num+=1
      if board[x][y] == opponent:
        opponent_num+=1

  return colour_num - opponent_num


def mock_move(player, board, x, y):
  if player == BLACK:
    colour = "black"
  else:
    colour = "white"
  temp_board = board
  temp_board[x][y] = colour
  temp_board = convertDiscs(temp_board, x, y)
  result = count_different(temp_board, player)
  return result

def generate_valid_moves(player, board):
  valid_moves = []
  for x in range(SIZE):
    for y in range(SIZE):
      if valid(board, player, x, y):
        valid_moves.append([x,y])
  return valid_moves

# calculate the mobility for opponent
def mobility(board, player):
  if player == BLACK:
    opponent = WHITE
  else:
    opponent = BLACK
  valid_moves = generate_valid_moves(opponent, board)
  return len(valid_moves)




#temporary poor hueristic
def tempHeuristic(board, player):
    score = 0
    corner_value = 50
    adjacent_value = 3
    side_value = 3
    # Set player and opponent colours
    if player == BLACK:
        colour = "black"
        opponent = "white"
    else:
        colour = "white"
        opponent = "black"


    # Basic hurisitc just use the number of pieces of the color they play on the board
    # as an indicator for the quality of a position. This greedy evaluation function is
    # derived from the final goal of the game: the player who has the most pieces wins. 
    # But this only makes sense if you really can look ahead until the end of the game 

    #
    difference_score = 4 * count_different(board, player)


    # A better criterion for determining a position is to count the number of moves a player can make: 
    # the mobility is decisive in Reversi! If you only have a few moves, it's likely that your opponent 
    # can play such that you are forced to make bad moves. Therefore, if your mobility is high, 
    # the position is better for you than if it's low.

    mobility_score = -5 * mobility(board, player)



    # Advanced huristic about edges and corner condition
    for x in range(SIZE):
        for y in range(SIZE):
            heuristic_value = 1

            if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
                if board[0][0] == colour:
                    heuristic_value = side_value
                else:
                    heuristic_value = -adjacent_value


            elif (x == 0 and y == 6) or (x == 1 and 6 <= y <= 7):
                if board[7][0] == colour:
                    heuristic_value = side_value
                else:
                    heuristic_value = -adjacent_value

            elif (x == 7 and y == 1) or (x == 6 and 0 <= y <= 1):
                if board[0][7] == colour:
                    heuristic_value = side_value
                else:
                    heuristic_value = -adjacent_value

            elif (x == 7 and y == 6) or (x == 6 and 6 <= y <= 7):
                if board[7][7] == colour:
                    heuristic_value = side_value
                else:
                    heuristic_value = -adjacent_value
           
            elif (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
                heuristic_value = side_value
            
            elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                heuristic_value = corner_value
         
            if board[x][y] == colour:
                score += heuristic_value
            elif board[x][y] == opponent:
                score -= heuristic_value
    return score + difference_score + mobility_score


#validity function
def valid(board, player, x, y):
    # Sets player colour
    if player == WHITE:
        colour = "white"
    else:
        colour = "black"

    if board[x][y] != None:
        return False

    else:
       
        neighbour = False
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, SIZE)):
            for j in range(max(0, y - 1), min(y + 2, SIZE)):
                if board[i][j] != None:
                    neighbour = True
                    neighbours.append([i, j])
    
        if not neighbour:
            return False
        else:
        
            valid = False
            for n in neighbours:

                neighbour_x = n[0]
                neighbour_y = n[1]

            
                if board[neighbour_x][neighbour_y] == colour:
                    continue
                else:
                    temp_x = neighbour_x
                    temp_y = neighbour_y

                    while 0 <= temp_x < SIZE and 0 <= temp_y < SIZE:
                     
                        if board[temp_x][temp_y] == None:
                            break
                        
                        if board[temp_x][temp_y] == colour:
                            valid = True
                            break
                        temp_x += neighbour_x - x
                        temp_y += neighbour_y - y
            return valid













