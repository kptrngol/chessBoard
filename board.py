import curses 
import random
import os
import json

def screenLayout(stdscr):
    start_y, start_x = stdscr.getmaxyx()
    start_y = start_y//8 
    start_x = start_x//8 
    basePositions = (start_y,start_x)
    return basePositions

def saveChessboard(pieces):
    # Create file for storing Chessboard setting with os module and bind it with setting var, also use with keyword to correctly close the operation
    with open("setting.json","w") as setting:
        # Use json module for dump setting into the tempfile
        json.dump(pieces,setting)

def loadChessboard():
    with open("setting.json", "r") as data:
        pieces = json.load(data)
        # Use list comprehension syntax for changing json lists in lists to tuples data type in Python
        pieces_parsed = [tuple(p) for p in pieces]
        return pieces_parsed

def generatingPosition():
    position_y = random.randint(0,7)
    position_x = random.randint(0,7)
    position = (position_y,position_x)
    return position

def checkOverlay(pieces):
    for p in pieces:
        overlay = pieces.count(p)
        if overlay >= 2:
            return True

def generatingPieces(stdscr):
    k = random.randint(1,5) + 1
    pieces = []
    while(True):
        pieces.clear()
        for p in range(k):
            position = generatingPosition()
            pieces.append(position)
        if (not checkOverlay(pieces)):
            break
    saveChessboard(pieces)
    return pieces
        

def printBoard(stdscr,pieces=[()]):

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    base = screenLayout(stdscr)

    heightCntr = 8
    widthCntr = 8

    # stdscr.addstr(0,0,f"{pieces}")

    # Printing 
    try:
        for y in range(8):
            for x in range(8):
                stdscr.addstr(2*base[0] + y,base[1] + x,"o")
        
        for p in pieces[0:len(pieces)]:
            stdscr.addstr(2*base[0] + p[0],base[1] + p[1],"q", curses.color_pair(1))

        pawn_position = pieces[-1]
        stdscr.addstr(2*base[0] + p[0],base[1] + p[1],"P", curses.color_pair(2))
    except Exception as e:
        pass
    showCapture(stdscr)

def generatePawn(stdscr):
    base = screenLayout(stdscr)
    pieces = loadChessboard()
    while(True):
        pawn_position = generatingPosition()
        pieces[-1] = pawn_position
        if (not checkOverlay(pieces)):
            break
    saveChessboard(pieces)
    printBoard(stdscr,pieces)

    stdscr.addstr(2*base[0] + pawn_position[0],base[1] + pawn_position[1],"P", curses.color_pair(2))
    showCapture(stdscr)

def removeQeen(stdscr):
    base = screenLayout(stdscr)
    pieces = loadChessboard()
    printBoard(stdscr, pieces)
    stdscr.addstr(2*base[0],3*base[1],"Provide the COLUMN of queen piece you would like to remove")
    x = int(stdscr.getkey())
    stdscr.addstr(2*base[0],3*base[1],"                                                             ")
    stdscr.addstr(2*base[0],3*base[1],"Provide the ROW of queen piece you would like to remove")
    y = int(stdscr.getkey())
    stdscr.addstr(2*base[0],3*base[1],"                                                             ")
    removedQueen = (y-1,x-1)
    try:
        for p in pieces:
            if (p == removedQueen):
                pieces.remove(p)
            stdscr.addstr(7*base[0],3*base[1],f"There is no qeen in that position {x,y}")
    except Exception as e:
        stdscr.addstr(7*base[0],3*base[1],f"There is no qeen in that position {x, y}")

    saveChessboard(pieces)
    printBoard(stdscr, pieces)
    showCapture(stdscr)

def showCapture(stdscr):
    base = screenLayout(stdscr)
    pieces = loadChessboard()
    pawn_position = pieces[-1]
    queensCapturing = []
    # printBoard(stdscr, pieces)
    for p in pieces[0:len(pieces)-1]:

        pieceRange = []
        
        # Horizontal and Vertical 
        for i in range(8):
            pieceRange.append((p[0],i))
            pieceRange.append((i,p[1])) 

        # Diagonal
        for i in range(1, 8):
            # upper right
            # For each iteration we check if y or x hit the chessboard border
            if p[0] - i >= 0 and p[1] + i <= 7:
                # Next we append all of these new positions which passed the test to the pieceRange list  
                pieceRange.append((p[0] - i, p[1] + i))
            # lower left
            if p[0] + i <= 7 and p[1] - i >= 0:
                pieceRange.append((p[0] + i, p[1] - i))
            # upper left
            if p[0] - i >= 0 and p[1] - i >= 0:
                pieceRange.append((p[0] - i, p[1] - i))
            # lower right
            if p[0] + i <= 7 and p[1] + i <= 7:
                pieceRange.append((p[0] + i, p[1] + i)) 
        
        # We remove p position two times, as we added them in horizontal and vertical range calculation
        pieceRange.remove(p)
        pieceRange.remove(p)
        pieceRange.append(pawn_position)
        
        if(checkOverlay(pieceRange)):
            stdscr.addstr(2*base[0] + p[0],base[1] + p[1],"q", curses.color_pair(3))
            queensCapturing.append(p)
    
    stdscr.addstr(8*base[0]-1,3*base[1],"                                                                                                                              ")
    stdscr.addstr(8*base[0]-1,3*base[1],f"Queens capturing pawn in (y,x) (0-7) orientation: {queensCapturing}")
    return queensCapturing

def testing(stdscr, results):
    base = screenLayout(stdscr)
    pieces = loadChessboard()
    printBoard(stdscr, pieces)
    queensCapturing = showCapture(stdscr)
    # Testing
    stdscr.addstr(8*base[0]-2,3*base[1],"                                                                                                                              ")
    stdscr.addstr(8*base[0]-2,3*base[1],f"Test results: {results}")




    



