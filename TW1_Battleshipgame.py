import sys
import os
import random
from colorama import Fore, Style

battlefieldsize = None

if "demo" in sys.argv:
    player1ships = {"h2": 0, "h3": 1, "h5": 0, "v2": 0, "v3": 0, "v5": 0}
    player2ships = {"h2": 0, "h3": 0, "h5": 0, "v2": 0, "v3": 1, "v5": 0}
else:
    player1ships = {"h2": 1, "h3": 1, "h5": 1, "v2": 1, "v3": 1, "v5": 1}
    player2ships = {"h2": 1, "h3": 1, "h5": 1, "v2": 1, "v3": 1, "v5": 1}


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


def creategrid(gridsize):
    grid = [["  ~" for i in range(gridsize)] for i in range(gridsize)]
    return grid


def showgrid(gridsize, grid):
    for i in range(gridsize + 1):
        if i == 0:
            sys.stdout.write(Style.BRIGHT + Fore.GREEN + '   ')
            continue
        if i == gridsize:
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


def placementprocess(grid, playerships):
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
            if 0 > x > battlefieldsize - 1:
                print('This coordinate is out of range!')
                continue
        except ValueError:
            print('incorrect input')
            continue
        try:
            y = int(input('Pick your ship\'s y coordinate: '))
            if 0 > y > battlefieldsize - 1:
                print('This coordinate is out of range!')
                continue
        except ValueError:
            print('incorrect input')
            continue
        if not place(x, y, grid, shiptype):
            continue
        else:
            playerships[shiptype] = playerships[shiptype] - 1
            break


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


def shootingprocess(gridsize, grid, grid_visible):
    print('Specify the coordinates of the target!')
    while True:
        try:
            x = int(input('x:'))
            if x > gridsize - 1:
                print('This coordinate is too large!')
                continue
            y = int(input('y:'))
            if y > gridsize - 1:
                print('This coordinate is too large!')
                continue
        except ValueError:
            print('incorrect input!')
            continue
        break
        os.system('clear')
    if shoot(x, y, grid, grid_visible):
        return 'You\'ve got a hit!'
    else:
        return 'You missed!'


def shoot(x, y, grid, grid_visible):
    if grid[y][x] == '  ⬜':
        grid_visible[y][x] = '  X'
        grid[y][x] = '  X'
        return True
    else:
        grid_visible[y][x] = '  0'
        return False


def sqarecheck(grid):
    count = 0
    for row in grid:
        for item in row:
            if item == '  ⬜':
                count += 1
    return count


# MAIN
os.system("clear")
if "demo" in sys.argv:
    print(Fore.RED + "=====BATTLESHIP GAME - DEMO=====>" + Fore.RESET)
else:
    print("=====BATTLESHIP GAME=====>")

while True:
    try:
        battlefieldsize = int(input("Enter gridsize..(int, >5 <11)"))
        if battlefieldsize > 5 and battlefieldsize < 11:
            break
        else:
            print ("this gridsize is invalid!")
            continue
    except ValueError:
        print('incorrect input!')
        continue

grid1 = creategrid(battlefieldsize)
grid2 = creategrid(battlefieldsize)
grid1_visible = creategrid(battlefieldsize)
grid2_visible = creategrid(battlefieldsize)

# -- Placement stage loop --

print('PLAYER 1 - PLACE YOUR SHIPS!')
showgrid(battlefieldsize, grid1)
displayships(player1ships)

while True:
    placementprocess(grid1, player1ships)
    showgrid(battlefieldsize, grid1)
    displayships(player1ships)

    player1ships_values = player1ships.values()
    ships_remaining = 0

    for item in player1ships_values:
        ships_remaining += item

    if ships_remaining == 0:
        break

os.system('clear')
print("PLAYER 1 - PLACEMENT COMPLETE!")
print('PLAYER 2 - PLACE YOUR SHIPS!')
showgrid(battlefieldsize, grid2)
displayships(player2ships)

while True:
    placementprocess(grid2, player2ships)
    showgrid(battlefieldsize, grid2)
    displayships(player2ships)

    player2ships_values = player2ships.values()
    ships_remaining = 0

    for item in player2ships_values:
        ships_remaining += item

    if ships_remaining == 0:
        break
os.system('clear')
print("PLAYER 2 - PLACEMENT COMPLETE!")
print()

# -- Shooting stage loop --
print("SHOOTING STAGE BEGINS!")
turncounter = 0
playertogo = random.randint(1, 2)

while True:
    if playertogo == 1:
        print("Player 1\'s turn!")
        showgrid(battlefieldsize, grid2_visible)
        print(shootingprocess(battlefieldsize, grid2, grid2_visible))
        showgrid(battlefieldsize, grid2_visible)
        if sqarecheck(grid2) == 0:
            print('Player 1 has won the game.')
            break
        playertogo = 2

    if playertogo == 2:
        print("Player 2\'s turn!")
        showgrid(battlefieldsize, grid1_visible)
        print(shootingprocess(battlefieldsize, grid1, grid1_visible))
        showgrid(battlefieldsize, grid1_visible)
        if sqarecheck(grid1) == 0:
            print('Player 2 has won the game.')
            break
        playertogo = 1
