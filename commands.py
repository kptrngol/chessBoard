import curses 
import sys
import board as b


def userCommand(stdscr):
    base = b.screenLayout(stdscr)
    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        # start_y, start_x = stdscr.getmaxyx()
        # start_y = start_y//8 
        # start_x = start_x//8 

        stdscr.addstr(2*base[0],3*base[1],"Manual")
        stdscr.addstr(2*base[0]+1,3*base[1]," ")
        stdscr.addstr(2*base[0]+2,3*base[1],"Function:............................................Command:")
        stdscr.addstr(2*base[0]+3,3*base[1],"Generate chessBoard with random queen and pawn positions:...b")
        stdscr.addstr(2*base[0]+4,3*base[1],"Generate new Pawn position..................................p")
        stdscr.addstr(2*base[0]+5,3*base[1],"Remove queen from specific position.........................r")
        stdscr.addstr(2*base[0]+6,3*base[1],"Exit........................................................e")

        stdscr.addstr(8*base[0],3*base[1],"Provide next command: .....", curses.color_pair(1))
    except Exception as e:
        stdscr.addstr(2*base[0],3*base[1],"Increase the terminal window")

    command = stdscr.getkey()
    return command

def performAction(stdscr,command):
    stdscr.clear()
    stdscr.refresh()

    match command:
        case "b":
            b.printBoard(stdscr, b.generatingPieces(stdscr))
        case "p":
            b.generatePawn(stdscr)
        case "r":
            b.removeQeen(stdscr)
        case "t":
            b.testing(stdscr, [(0,0),(0,7),(7,0),(7,7)])          
        case "e" | "exit":
            sys.exit(0)
        case _:
            base = b.screenLayout(stdscr)
            stdscr.addstr(8*base[0]+1,3*base[1],"Try again!")
