import sys
import os
import bslib  # local module


GRIDSIZE = 10  # 10 makes the most sense, ship placement is possible and does not take too long
AImode = False

if "demo" in sys.argv:
    player1ships = {"h2": 0, "h3": 1, "h5": 0, "v2": 0, "v3": 0, "v5": 0}
    player2ships = {"h2": 0, "h3": 0, "h5": 0, "v2": 0, "v3": 1, "v5": 0}
else:
    player1ships = {"h2": 1, "h3": 1, "h5": 1, "v2": 1, "v3": 1, "v5": 1}
    player2ships = {"h2": 1, "h3": 1, "h5": 1, "v2": 1, "v3": 1, "v5": 1}


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

grid1 = bslib.creategrid(GRIDSIZE)
grid2 = bslib.creategrid(GRIDSIZE)
grid1_visible = bslib.creategrid(GRIDSIZE)
grid2_visible = bslib.creategrid(GRIDSIZE)

# -- Placement stage loop --

print('PLAYER 1 - PLACE YOUR SHIPS!')
bslib.showgrid(GRIDSIZE, grid1)
bslib.displayships(player1ships)

while True:
    if gamemode == 1:
        bslib.placementprocess(grid1, GRIDSIZE, player1ships, gamemode)
        bslib.showgrid(GRIDSIZE, grid1)
        break
    else:
        bslib.placementprocess(grid1, GRIDSIZE, player1ships)
        bslib.showgrid(GRIDSIZE, grid1)
        bslib.displayships(player1ships)

    player1ships_values = player1ships.values()
    ships_remaining = 0

    for item in player1ships_values:
        ships_remaining += item

    if ships_remaining == 0:
        break

os.system('clear')
print("PLAYER 1 - PLACEMENT COMPLETE!")
print('PLAYER 2 - PLACE YOUR SHIPS!')
bslib.showgrid(GRIDSIZE, grid2)
bslib.displayships(player2ships)

while True:
    bslib.placementprocess(grid2, GRIDSIZE, player2ships)
    bslib.showgrid(GRIDSIZE, grid2)
    bslib.displayships(player2ships)

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
        bslib.showgrid(GRIDSIZE, grid2_visible)
        print(shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode))
        bslib.showgrid(GRIDSIZE, grid2_visible)

        if sqarecheck(grid2) == 0:
            print('Player 1 has won the game.')
            break
        playertogo = 2

    elif playertogo == 1:
        print("Player 1\'s turn!")
        bslib.showgrid(GRIDSIZE, grid2_visible)
        print(shootingprocess(GRIDSIZE, grid2, grid2_visible))
        bslib.showgrid(GRIDSIZE, grid2_visible)
        if sqarecheck(grid2) == 0:
            print('Player 1 has won the game.')
            break
        playertogo = 2

    if playertogo == 2:
        print("Player 2\'s turn!")
        bslib.showgrid(GRIDSIZE, grid1_visible)
        print(shootingprocess(GRIDSIZE, grid1, grid1_visible))
        bslib.showgrid(GRIDSIZE, grid1_visible)
        if sqarecheck(grid1) == 0:
            print('Player 2 has won the game.')
            break
        playertogo = 1
