"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    # data = {}
    data["rows"] = 10
    data["cols"] = 10
    data["boardsize"] = 500
    data["cellsize"] = data["boardsize"]/data["rows"]
    data["userboard"] = emptyGrid(data["rows"], data["cols"])
    data["computerboard"] = emptyGrid(data["rows"], data["cols"])
    data["numberofships"] = 5
    data["computerboard"] = addShips(data["computerboard"], data["numberofships"])
    data["tempship"] = []
    data["usership"] = 0
    return data


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userboard"], True)
    drawGrid(data, compCanvas, data["computerboard"], False) 
    drawShip(data, userCanvas, data["tempship"])
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    ccell = getClickedCell(data, event)
    if board == "user":
        clickUserBoard(data, ccell[0], ccell[1])
    if board == "comp":
        runGameTurn(data, ccell[0], ccell[1])
    pass

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for i in range(rows):
        innerlst = []
        for j in range(cols):
            innerlst.append(1)
        grid.append(innerlst)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
import random
def createShip():
    r = random.randint(1,8)
    c = random.randint(1,8)
    shipOrientation = random.randint(0,1)
    if shipOrientation == 0:
        ship = [[r-1,c],[r,c],[r+1,c]]
    else:
        ship = [[r,c-1],[r,c],[r,c+1]]
    return ship



'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for x in ship:
        if grid[x[0]][x[1]]!= EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count < numShips:
        new = createShip()
        lst = checkShip(grid,new)
        if lst == True:
            for y in new:
                grid[y[0]][y[1]] = SHIP_UNCLICKED
            count += 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for a in range(data["rows"]):
        for b in range(data["cols"]):
            if grid[a][b] == SHIP_UNCLICKED:
                if showShips == True:
                    canvas.create_rectangle(b*data["cellsize"],a*data["cellsize"], data["cellsize"] * (b+1), (a+1) * data["cellsize"], fill="yellow")
                else:
                    canvas.create_rectangle(b*data["cellsize"],a*data["cellsize"], data["cellsize"] * (b+1), (a+1) * data["cellsize"], fill="blue")
            elif grid[a][b] == SHIP_CLICKED:
                 canvas.create_rectangle(b*data["cellsize"],a*data["cellsize"], data["cellsize"] * (b+1), (a+1) * data["cellsize"], fill="red")
            elif grid[a][b] == EMPTY_CLICKED:
                 canvas.create_rectangle(b*data["cellsize"],a*data["cellsize"], data["cellsize"] * (b+1), (a+1) * data["cellsize"], fill="white")
            else:
                canvas.create_rectangle(b*data["cellsize"],a*data["cellsize"], data["cellsize"] * (b+1), (a+1) * data["cellsize"], fill="blue")

### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    i=0
    if ship[i][1]==ship[i+1][1]==ship[i+2][1]:
        ship.sort()
        if ship[i+1][0]-ship[i][0]==1 and ship[i+2][0]-ship[i+1][0]==1:
            return True
    return False

'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    i=0
    if ship[i][0]==ship[i+1][0]==ship[i+2][0]:
        ship.sort()
        if ship[i+1][1]-ship[i][1]==1 and ship[i+2][1]-ship[i+1][1]==1:
            return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    csize=int(data["cellsize"])
    x_cordinate = event.x
    y_cordinate = event.y
    data["getClickedCell"] = [int(event.y/csize), int(event.x/csize)]
    return data["getClickedCell"]
    
'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for a in ship: 
        fst=a[0] 
        sec=a[1] 
        canvas.create_rectangle(sec * data["cellsize"],fst * data["cellsize"], (1 + sec) * data["cellsize"], (fst + 1)*data["cellsize"], fill="white")
    return 
   


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    v = isVertical(ship)
    h = isHorizontal(ship)
    cship=checkShip(grid, ship)
    if cship == True:
        if len(ship) == 3:
            if v == True or h == True:
                return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    egrid = data["userboard"]
    if shipIsValid(egrid, data["tempship"]) == True:
        for x in data["tempship"]:
            egrid[x[0]][x[1]] = SHIP_UNCLICKED
        data["usership"] = data["usership"] + 1
    else:
        print("ship is not valid")
    data["tempship"] =[]    
    return 

'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    rc=data["userboard"]
    if [row,col] in rc or data["usership"] == 5:
        return
    data["tempship"].append([row,col])
    if len(data["tempship"]) == 3:
        placeShip(data)
    if data["usership"] == 5:
        print("you can start the game")
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    else:
        board[row][col] == EMPTY_UNCLICKED
        board[row][col] = EMPTY_CLICKED
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    u=data["userboard"]
    c=data["computerboard"]
    if c[row][col] == SHIP_CLICKED or c[row][col] == EMPTY_CLICKED:
        return
    else:
        return updateBoard(data, c, row, col, "user")

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    return


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    test.testUpdateBoard()



    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)


