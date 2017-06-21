import sys
import os
import random
from colorama import Fore, Style

GRIDSIZE = 10  # 10 makes the most sense, ship placement is possible and does not take too long
AImode = False

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


def placementprocess(grid, playerships, placement_mode=2):
    if placement_mode == 1:
        while True:
            AI_shiplist = []  # The AI will also work if more than 1 of each shiptype is present
            for key, value in player1ships.items():
                i = 0
                while i < value:
                    if not place(generate_cordinates(GRIDSIZE), generate_cordinates(GRIDSIZE), grid, key):
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
            if 0 > x > grid_size - 1:
                print('This coordinate is out of range!')
                continue
        except ValueError:
            print('incorrect input')
            continue
        try:
            y = int(input('Pick your ship\'s y coordinate: '))
            if 0 > y > grid_size - 1:
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


def shootingprocess(grid_size, grid, grid_visible, mode=False):
    if mode:
        if shoot(generate_cordinates(grid_size), generate_cordinates(grid_size), grid, grid_visible):
            return 'AI\'s got a hit!'
        else:
            return 'AI missed!'

    print('Specify the coordinates of the target!')
    while True:
        try:
            x = int(input('x:'))
            if x > grid_size - 1:
                print('This coordinate is too large!')
                continue
            y = int(input('y:'))
            if y > grid_size - 1:
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
        gamemode = int(input("Please choose game mode: AI = 1 or Players = 2:  "))
        if gamemode < 1 or gamemode > 2:
            print ("This gamemode is invalid, please try again!")
            continue
    except ValueError:
        print('incorrect input!')
        continue
    if gamemode == 1:
        AImode = True
    break

grid1 = creategrid(GRIDSIZE)
grid2 = creategrid(GRIDSIZE)
grid1_visible = creategrid(GRIDSIZE)
grid2_visible = creategrid(GRIDSIZE)

# -- Placement stage loop --

print('PLAYER 1 - PLACE YOUR SHIPS!')
showgrid(GRIDSIZE, grid1)
displayships(player1ships)

while True:
    if gamemode == 1:
        placementprocess(grid1, player1ships, gamemode)
        showgrid(GRIDSIZE, grid1)
        break
    else:
        placementprocess(grid1, player1ships)
        showgrid(GRIDSIZE, grid1)
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
showgrid(GRIDSIZE, grid2)
displayships(player2ships)

while True:
    placementprocess(grid2, player2ships)
    showgrid(GRIDSIZE, grid2)
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
    if playertogo == 1 and AImode:
        print("AI\'s turn!")
        showgrid(GRIDSIZE, grid2_visible)
        print(shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode))
        showgrid(GRIDSIZE, grid2_visible)

        if sqarecheck(grid2) == 0:
            print('Player 1 has won the game.')
            break
        playertogo = 2

    elif playertogo == 1:
        print("Player 1\'s turn!")
        showgrid(GRIDSIZE, grid2_visible)
        print(shootingprocess(GRIDSIZE, grid2, grid2_visible))
        showgrid(GRIDSIZE, grid2_visible)
        if sqarecheck(grid2) == 0:
            print('Player 1 has won the game.')
            break
        playertogo = 2

    if playertogo == 2:
        print("Player 2\'s turn!")
        showgrid(GRIDSIZE, grid1_visible)
        print(shootingprocess(GRIDSIZE, grid1, grid1_visible))
        showgrid(GRIDSIZE, grid1_visible)
        if sqarecheck(grid1) == 0:
            print('Player 2 has won the game.')
            break
        playertogo = 1
