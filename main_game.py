from tkinter import *
from gui import *
from moves import *


#function to start the game
runGame()

# Binding the buttons using handlers
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>", keyHandle)
screen.focus_set()

# tkinter function to catch events and run the program
game.wm_title("Othello")
game.mainloop()


















