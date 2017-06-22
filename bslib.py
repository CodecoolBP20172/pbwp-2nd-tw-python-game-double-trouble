import sys
from colorama import Fore, Style
import random


def displayships(listofships):
    print(Style.BRIGHT + "Your available ships: \n")
    print("⬜ " + Fore.RED + "⬜" + Fore.WHITE + "    ⬜ ⬜ " + Fore.RED + "⬜" +
          Fore.WHITE + "    ⬜ ⬜ ⬜ ⬜ " + Fore.RED + "⬜")
    print(Fore.RESET +
          "h2 " +
          str(listofships["h2"]) +
          "x  h3 " +
          str(listofships["h3"]) +
          "x    h5 " +
          str(listofships["h5"]) +
          "x    ")
    print()
    print("                ⬜")
    print("                ⬜")   # Don't mind that its not alligned here, its still
    print("         ⬜      ⬜")  # alligned fine in the terminal
    print("  ⬜      ⬜      ⬜")
    print(Fore.RED + "  ⬜      ⬜      ⬜")
    print(Fore.RESET + "v2 " + str(listofships["v2"]) + "x  v3 " +
          str(listofships["v3"]) + "x  v5 " + str(listofships["v5"]) + "x")


def creategrid(grid_size):
    grid = [["  ~" for i in range(grid_size)] for i in range(grid_size)]
    return grid


def showgrid(grid_size, grid):
    for i in range(grid_size + 1):
        if i == 0:
            sys.stdout.write(Style.BRIGHT + Fore.GREEN + '   ')
            continue
        if i == grid_size:
            print(' ', str(i - 1) + Fore.RESET)
            break
        sys.stdout.write(str('{:3}'.format(i - 1)))
    for rownum, row in enumerate(grid):
        sys.stdout.write(Fore.GREEN + '{:3}'.format(rownum) + Fore.RESET)
        for colnum, item in enumerate(row):
            if item == '  X':
                sys.stdout.write(Fore.RED + '{:3}'.format(item) + Fore.RESET)
            else:
                sys.stdout.write(Fore.BLUE + '{:3}'.format(item) + Fore.RESET)
        sys.stdout.write('\n')


def validateposition(grid, direction, units, x0, y0):
    x = x0
    y = y0
    if direction == 'h':
        for i in range(units):
            if grid[y][x] == '  ⬜':
                return False
            x -= 1
    if direction == 'v':
        for i in range(units):
            if grid[y][x] == '  ⬜':
                return False
            y -= 1
    return True


def generate_cordinates(grid_size):
    return random.randint(0, grid_size-1)


def placementprocess(grid, grid_size, playerships, placement_mode=2):
    if placement_mode == 1:
        while True:
            AI_shiplist = []  # The AI will also work if more than 1 of each shiptype is present
            for key, value in playerships.items():
                i = 0
                while i < value:
                    if not place(generate_cordinates(grid_size), generate_cordinates(grid_size), grid, key):
                        continue
                    else:
                        i += 1

            return

    while True:

        shiptype = input('Choose shiptype: ')
        if shiptype not in playerships or playerships[shiptype] == 0:
            print(
                'You don\'t have any more from this shiptype or your input is not recognized!')
            continue
        else:
            break
    while True:
        try:
            x = int(input('Pick your ship\'s x coordinate: '))
            if x > grid_size-1 or x < 0:
                print('This coordinate is out of range!')
                continue
        except ValueError:
            print('incorrect input')
            continue
        try:
            y = int(input('Pick your ship\'s y coordinate: '))
            if y > grid_size-1 or y < 0:
                print('This coordinate is out of range!')
                continue
        except ValueError:
            print('incorrect input')
            continue
        if not place(x, y, grid, shiptype):
            continue
        else:
            playerships[shiptype] = playerships[shiptype] - 1
            return


def place(x, y, grid, shiptype):
    if shiptype == 'v2':
        if y == 0 or not validateposition(grid, 'v', 2, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y - 1][x] = '  ⬜'
        return True
    if shiptype == 'h2':
        if x == 0 or not validateposition(grid, 'h', 2, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y][x - 1] = '  ⬜'
        return True
    if shiptype == 'v3':
        if y < 2 or not validateposition(grid, 'v', 3, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y - 1][x] = '  ⬜'
        grid[y - 2][x] = '  ⬜'
        return True
    if shiptype == 'h3':
        if x < 2 or not validateposition(grid, 'h', 3, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y][x - 1] = '  ⬜'
        grid[y][x - 2] = '  ⬜'
        return True
    if shiptype == 'v5':
        if y < 4 or not validateposition(grid, 'v', 5, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y - 1][x] = '  ⬜'
        grid[y - 2][x] = '  ⬜'
        grid[y - 3][x] = '  ⬜'
        grid[y - 4][x] = '  ⬜'
        return True
    if shiptype == 'h5':
        if x < 4 or not validateposition(grid, 'h', 5, x, y):
            print('That ship will not fit there!')
            return False
        grid[y][x] = '  ⬜'
        grid[y][x - 1] = '  ⬜'
        grid[y][x - 2] = '  ⬜'
        grid[y][x - 3] = '  ⬜'
        grid[y][x - 4] = '  ⬜'
        return True
