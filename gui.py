from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from moves import *
from game_canvas import *



SIZE = 8
WHITE = 0
BLACK = 1
nodes = 0
depth = 5
GRID_ROW = 450
GRID_COLUMN = 50




class GameBoard:
    def __init__(self):
        self.player = WHITE
        self.noValidMoves = False
        self.won = False
        # Initializing the game board
        self.board = [[None for i in range(SIZE)] for j in range(SIZE)]
        self.board[3][3] = "white"
        self.board[3][4] = "black"
        self.board[4][3] = "black"
        self.board[4][4] = "white"
        self.oldboard = self.board

    
# updates the state of game after every move
# flips the discs on every move. 
    def update(self):
        # Clear the board
        screen.delete("valids")
        screen.delete("disc")

        for x in range(SIZE):
            for y in range(SIZE):

                # Create initial discs of white and black
                if self.oldboard[x][y] == "white":
                    create_white_discs(x,y,"disc {0}-{1}".format(x, y));
                elif self.oldboard[x][y] == "black":
                    create_black_discs(x,y,"disc {0}-{1}".format(x, y));
                  

        screen.update()
        for x in range(SIZE):
            for y in range(SIZE):
                
             
                if self.board[x][y] != self.oldboard[x][y] and self.board[x][y] == "white":
                    screen.delete("{0}-{1}".format(x, y))
             
                    print ("board", self.board[x][y])
                    print("oldboard", self.oldboard[x][y])
                  
                    create_white_discs(x,y,"disc create")

                   
                    sleep(0.01)
                    screen.update()
                    screen.delete("create")
                  
                    create_white_discs(x,y,"disc")
                    screen.update()

                elif self.board[x][y] != self.oldboard[x][y] and self.board[x][y] == "black":
                    screen.delete("{0}-{1}".format(x, y))
                  
                
                    create_black_discs(x,y,"disc create")
                  
                    sleep(0.01)
                    screen.update()
                    screen.delete("create")

                    create_black_discs(x,y,"disc")
                    screen.update()

        # Drawing of valid circles
        for x in range(SIZE):
            for y in range(SIZE):
                if self.player == WHITE:
                    if valid(self.board, self.player, x, y):
                        screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                           tags="valids", fill="yellow", outline="#008000")

        # Function for AI agent to make a move.
        if not self.won:
            self.scoreBoard()
            screen.update()
            if self.player == BLACK:
                startTime = time()
                self.oldboard = self.board
                alpha = float('-inf')
                beta = float('inf')
                result = self.alphaBeta(self.board, depth, alpha, beta, 1)
                self.board = result[1]

                if len(result) == 3:
                    pos = result[2]
                    self.oldboard[pos[0]][pos[1]] = "black"

                self.player = 1 - self.player
                deltaTime = round((time() - startTime))
                if deltaTime < 2:
                    sleep(2 - deltaTime)
                nodes = 0
                # Player must pass?
                self.noValidMovesRemaining()
        else:
             screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="Game won")
            # tkinter.messagebox.showinfo("Title", "a Tk MessageBox " )



# function to make game moves
    def makeMove(self, x, y):
        global nodes
        # Move and update screen
        self.oldboard = self.board
        self.oldboard[x][y] = "white"
        self.board = convertDiscs(self.board, x, y)

        # Switch Player
        self.player = 1 - self.player
        self.update()

        self.noValidMovesRemaining()
        self.update()

    def scoreBoard(self):
        # global moves
        global player_score


        # Deleting prior score elements
        screen.delete("score")

        # Scoring based on number of discs
        player_score = 0
        computer_score = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.board[x][y] == "white":
                    player_score += 1
                elif self.board[x][y] == "black":
                    computer_score += 1

        if self.player == WHITE:
            current_colour = "white"
          
        else:
            current_colour = "black"
       

        screen.create_text(230 , 550, anchor="c", tags="score",text=current_colour, font=("Georgia", 25), fill=current_colour)
        screen.create_text(30, 550, anchor="w", tags="score", font=("Georgia", 50), fill="white",
                           text=player_score)
        screen.create_text(400, 550, anchor="w", tags="score", font=("Georgia", 50), fill="black",
                           text=computer_score)

        

    # function to determine if a player can play his turn or needs to pass it to its opponent
    def noValidMovesRemaining(self):
        passTurn = True
        for x in range(SIZE):
            for y in range(SIZE):
                if valid(self.board, self.player, x, y):
                    passTurn = False
        if passTurn:
            self.player = 1 - self.player
            if self.noValidMoves == True:
                self.won = True
            else:
                self.noValidMoves = True
            self.update()
        else:
            self.noValidMoves = False


     #Alpha beta prunning function .
     # It creates a mock game upto a certain depth i.e it traverse the possible moves upto a given depth 
     # and uses alpha beta prunning to optimize the traversal
    def alphaBeta(self, node, depth, alpha, beta, maxim):
        global nodes
        nodes += 1
        boards = []
        choices = []

        for x in range(SIZE):
            for y in range(SIZE):
                if valid(self.board, self.player, x, y):
                    test = convertDiscs(node, x, y)
                    boards.append(test)
                    choices.append([x, y])

        # Every combination on the board has a value which can be determined by heuristic function
        if depth == 0 or len(choices) == 0:
            return ([tempHeuristic(node, maxim), node])

        if maxim:
            v = -float("inf")
            opt_board = []
            opt_choice = []
            for brd in boards:
                boardValue = self.alphaBeta(brd, depth - 1, alpha, beta, 0)[0]
                if boardValue > v:
                    v = boardValue
                    
                    opt_board = brd
                    opt_choice = choices[boards.index(brd)]
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return ([v, opt_board, opt_choice])
        else:
            v = float("inf")
            opt_board = []
            opt_choice = []
            for brd in boards:
                boardValue = self.alphaBeta(brd, depth - 1, alpha, beta, 1)[0]
                if boardValue < v:
                    v = boardValue
                    opt_board = brd
                    opt_choice = choices[boards.index(brd)]
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return ([v, opt_board, opt_choice])




# function to determine which discs to convert
def convertDiscs(passedArray, x, y):
    board = deepcopy(passedArray)
    if gameboard.player == WHITE:
        colour = "white"

    else:
        colour = "black"
    board[x][y] = colour

    # finding the neighbours
    neighbours = []
    for i in range(max(0, x - 1), min(x + 2, SIZE)):
        for j in range(max(0, y - 1), min(y + 2, SIZE)):
            if board[i][j] != None:
                neighbours.append([i, j])

    # Which discs to convert
    convert_discs = []

    #Position of the discs to be flipped
    for n in neighbours:
        neighbour_x = n[0]
        neighbour_y = n[1]
        
        if board[neighbour_x][neighbour_y] != colour:
           
            disc_path = []
            dirX = neighbour_x - x
            dirY = neighbour_y - y
          
            while 0 <= neighbour_x < SIZE and 0 <= neighbour_y < SIZE:
                disc_path.append([neighbour_x, neighbour_y])
                value = board[neighbour_x][neighbour_y]
               
                if value == None:
                    break
          
                if value == colour:
                   
                    for node in disc_path:
                        convert_discs.append(node)
                    break
              
                neighbour_x += dirX
                neighbour_y += dirY

    # change discs
    for node in convert_discs:
        board[node[0]][node[1]] = colour

    return board


    screen.update()


def playGame():
    global gameboard, running
    running = True
    screen.delete(ALL)
    restart()
    gameboard = 0

    gridBoard()

    gameboard = GameBoard()
    #Update gameboard on every change
    gameboard.update()

def keyHandle(event):
    symbol = event.keysym
    if symbol.lower() == "r":
        playGame()



def gridBoard():

    #outline
    screen.create_rectangle(50, 50, 450, 450, outline="black", width=5, fill="green")

    # Drawing the intermediate lines
    for i in range(SIZE-1):
        line_spacing = 50 + 50 * (i + 1)

        # Horizontal line
        screen.create_line(GRID_COLUMN, line_spacing, GRID_ROW, line_spacing, fill="#111")

        # Vertical line
        screen.create_line(line_spacing, GRID_COLUMN, line_spacing, GRID_ROW, fill="#111")



# functio to hadle button clicks
def clickHandle(event):
    global depth
    x_pointer = event.x
    y_pointer = event.y
    if running:
        if x_pointer >= GRID_ROW and y_pointer <= GRID_COLUMN:
            game.destroy()
        elif x_pointer <= GRID_COLUMN and y_pointer <= GRID_COLUMN:
            playGame()
        else:
            if gameboard.player == WHITE:
                # Delete the highlights
                x = int((event.x - 50) / 50)
                y = int((event.y - 50) / 50)
        
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    if valid(gameboard.board, gameboard.player, x, y):
                        gameboard.makeMove(x, y)
    else:
        # Index where mouse was clicked - Levels
        if 300 <= y_pointer <= 350:
 
            if 25 <= x_pointer <= 155:
                depth = 1
                playGame()
       
            elif 180 <= x_pointer <= 310:
                depth = 3
                playGame()
            
            elif 335 <= x_pointer <= 465:
                depth = 5
                playGame()

#function to start the game
def runGame():
   
    
    global running
    running = False
    # Title and shadow
    screen.create_text(250, 203, anchor="c", text="Othello", font=("Georgia", 50, "bold italic"), fill="black")
    screen.create_text(250, 200, anchor="c", text="Othello", font=("Georgia", 50, "bold italic"), fill="yellow")

    # Creating the difficulty buttons
    for i in range(3):
        # Background
        screen.create_rectangle(25 + 155 * i, 310, 155 + 155 * i, 355, fill="#000", outline="#000")
        screen.create_rectangle(25 + 155 * i, 300, 155 + 155 * i, 350, fill="#111", outline="#111")

        spacing = 130 / (0.005*i+ 2 )
       
            # Star with double shadow
        screen.create_text(25 +  spacing + 155 * i, 326, anchor="c", text="Level "+ str(i + 1), font=("Georgia", 25),
                               fill="yellow")
        

    screen.update()

#function to create white discs
def create_white_discs(x,y,tag_name):
    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags=tag_name, fill="#fff", outline="#aaa")

#function to create black discs
def create_black_discs(x,y,tag_name):
    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags=tag_name, fill="#111", outline="#000")



