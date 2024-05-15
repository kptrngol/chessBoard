import curses
import commands as c
import board as b

def main(stdscr):
    while(1):
        c.performAction(stdscr,c.userCommand(stdscr))

curses.wrapper(main)

# sdrscr jest obiektem tworzonym automatycznie przez funkcję wrapper 
# następnie przekazany do funkcji main, która na tym obiekcie pracuje
# Aktywuję widok curses

