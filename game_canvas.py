from copy import deepcopy
from tkinter import *


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600


#Creates a canvas of the game
game = Tk()
screen = Canvas(game, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="gray12", highlightthickness=0)
screen.pack()


# Creates the restart button
def restart():
    screen.create_rectangle(5, 5, 94, 45, fill="gray10", outline="gray", width=4)
    screen.create_text(50,25,text = "Restart", font=("Georgia", 15,"bold italic"), fill="yellow")

   




