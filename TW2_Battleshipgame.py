import sys
import os
import random
import bslib  # local module

# Global stuff declaration

GRIDSIZE = 10  # 10 makes the most sense, ship placement is possible and does not take too long
AImode = False  # switch to control AI mode for functions
AI_primarypoint = tuple  # The AI remembers and uses the coords of the first hit
AI_hitcounter = 0  # to count the number of consecutive hits
AI_directionlist = []  # stores generated direction data
AI_instructionlist = []  # the AI uses this list to properly guess ship positions upon hitting
AI_direction = tuple  # controls the direction of attempts from the first hit
AI_state = "RANDOM"  # possible states: RANDOM, FIRST_HIT, TURN_AROUND, MULTIPLE_HITS, CHANGE_DIR

if "demo" in sys.argv:
    player1ships = {"h2": 0, "h3": 1, "h5": 0, "v2": 0, "v3": 0, "v5": 0}
    player2ships = {"h2": 0, "h3": 0, "h5": 0, "v2": 0, "v3": 1, "v5": 0}
else:
    player1ships = {"h2": 1, "h3": 1, "h5": 1, "v2": 1, "v3": 1, "v5": 1}
    player2ships = {"h2": 0, "h3": 0, "h5": 2, "v2": 0, "v3": 0, "v5": 1}


def debug_printAIdata():
    print("STATE: ", AI_state)
    print("primary point: ", AI_primarypoint)
    print('hitcount: ', AI_hitcounter)
    print('directionlist: ', AI_directionlist)
    print('direction: ', AI_direction)
    print('instructionlist: ', AI_instructionlist)


def shootingprocess(grid_size, grid, grid_visible, AI_mode=False, coordinates=None):
    if AI_mode:
        if coordinates is None:  # check if we've got coordinates, if none then generate random
            x = bslib.generate_cordinates(grid_size)
            y = bslib.generate_cordinates(grid_size)
        else:  # if yes then use these instead of generating
            x = coordinates[0]
            y = coordinates[1]
        if shoot(x, y, grid, grid_visible):
            return x, y
        else:
            return None

    print('Specify the coordinates of the target!')
    while True:
        try:
            x = int(input('x:'))
            if x > grid_size-1 or x < 0:
                print('This coordinate is out of range!')
                continue
            y = int(input('y:'))
            if y > grid_size-1 or y < 0:
                print('This coordinate is out of range!')
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


def AI_rolldirection():
    AI_directionlist.clear()
    dice = random.randint(1, 4)
    if dice == 1:
        return [(0, -1), (1, 0), (0, 1), (-1, 0)]  # down, right, up, left
    if dice == 2:
        return [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, up, left, down
    if dice == 3:
        return [(-1, 0), (0, -1), (1, 0), (0, 1)]  # left, down, right, up
    if dice == 4:
        return [(0, 1), (-1, 0), (0, -1), (1, 0)]  # up, left, down, right


def AI_makeinstructionlist(coord, direction, howmanytimes):
    if howmanytimes == 0:  # stopping condition for the recursion
        return
    else:
        item = tuple(x+y for x, y in zip(coord, direction))
        AI_instructionlist.append(item)
        AI_makeinstructionlist(item, direction, howmanytimes-1)


def validatecoordinate(grid_size, coordinate, grid):
    for coord in coordinate:
        if coord > grid_size-1 or coord < 0:
            return "TURN_AROUND"
    for coord in coordinate:
        if grid[coordinate[1]][coordinate[0]] == '  0':
            return "CHANGE_DIR"
    return None


def resolve_AI_state(state):

    if state == "CHANGE_DIR":
        print('resolving CHANGE_DIR...')
        AI_instructionlist.clear()
        try:
            AI_direction = AI_directionlist.pop(0)
        except IndexError:
            AI_directionlist.clear()
            AI_state = "RANDOM"
            print('new AI state is: ', AI_state)
            return

        print("changed direction to: ", AI_direction)

        AI_makeinstructionlist(AI_primarypoint, AI_direction, 5)
        print('resolved CHANGE_DIR.')

    elif state == "TURN_AROUND":
        print('resolving TURN_AROUND...')
        try:
            AI_direction = AI_directionlist.pop(1)
        except IndexError:
            AI_directionlist.clear()
            AI_state = "RANDOM"
            print('new AI state is: ', AI_state)
            return
        print("changed direction to: ", AI_direction)

        AI_makeinstructionlist(AI_primarypoint, AI_direction, 5)
        AI_hitcounter = 1
        print('resolved TURN_AROUND.')
    else:
        print('no resolving exists for this state: ', state)
        sys.exit('Program will now terminate :( )')
#  >>>>>>> MAIN <<<<<<<<


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
    if playertogo == 1 and AImode:  # begin AI block
        print("AI\'s turn!")

        if AI_state == "FIRST_HIT":
            while True:
                if AI_state == "RANDOM":  # Resolving a previous state can produce this state
                    next_coord = None
                    break
                else:
                    next_coord = AI_instructionlist[AI_hitcounter-1]
                    validationresult = validatecoordinate(GRIDSIZE, next_coord, grid2_visible)
                    if validationresult is None:
                        print('coordinate validated!')
                        break
                    else:
                        print('coordinate validation failed!', next_coord)
                        resolve_AI_state(validationresult)
                    continue

            result = shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode, coordinates=next_coord)
            if type(result) == tuple:  # we have a hit, function returned tuple
                AI_hitcounter += 1
                AI_state = "MULTIPLE_HITS"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2
            else:  # we have a miss, change direction
                AI_state = "CHANGE_DIR"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2

        if AI_state == "MULTIPLE_HITS" and playertogo == 1:
            while True:
                if AI_state == "RANDOM":  # Resolving a previous state can produce this state
                    next_coord = None
                    break
                else:
                    next_coord = AI_instructionlist[AI_hitcounter-1]
                    validationresult = validatecoordinate(GRIDSIZE, next_coord, grid2_visible)
                    if validationresult is None:
                        print('coordinate validated!')
                        break
                    else:
                        print('coordinate validation failed!', next_coord)
                        resolve_AI_state(validationresult)
                    continue

            result = shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode, coordinates=next_coord)
            if type(result) == tuple:  # we have a hit, function returned tuple
                AI_hitcounter += 1
                AI_state = "MULTIPLE_HITS"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2
            else:  # we have a miss, check number of hits and decide based on that
                if AI_hitcounter > 4:
                    print('max. allowed consecutive hits reached! switching to RANDOM')
                    AI_state = "RANDOM"
                    AI_instructionlist.clear()
                    AI_hitcounter = 0
                    debug_printAIdata()
                    bslib.showgrid(GRIDSIZE, grid2_visible)
                    playertogo = 2
                else:
                    AI_state = "TURN_AROUND"
                    debug_printAIdata()
                    bslib.showgrid(GRIDSIZE, grid2_visible)
                    playertogo = 2

        if AI_state == "CHANGE_DIR" and playertogo == 1:
            resolve_AI_state("CHANGE_DIR")
            AI_hitcounter = 1
            while True:
                if AI_state == "RANDOM":  # Resolving a previous state can produce this state
                    next_coord = None
                    break
                else:
                    next_coord = AI_instructionlist[AI_hitcounter-1]
                    validationresult = validatecoordinate(GRIDSIZE, next_coord, grid2_visible)
                    if validationresult is None:
                        print('coordinate validated!')
                        break
                    else:
                        print('coordinate validation failed!', next_coord)
                        resolve_AI_state(validationresult)
                    continue

            result = shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode, coordinates=next_coord)
            if type(result) == tuple:  # we have a hit, function returned tuple
                AI_hitcounter += 1
                AI_state = "MULTIPLE_HITS"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2
            else:  # we have a miss, keep changing direction!
                AI_state = "CHANGE_DIR"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2

        if AI_state == "TURN_AROUND" and playertogo == 1:
            resolve_AI_state("TURN_AROUND")
            while True:
                if AI_state == "RANDOM":  # Resolving a previous state can produce this state
                    next_coord = None
                    break
                else:
                    next_coord = AI_instructionlist[AI_hitcounter-1]
                    validationresult = validatecoordinate(GRIDSIZE, next_coord, grid2_visible)
                    if validationresult is None:
                        print('coordinate validated!')
                        break
                    else:
                        print('coordinate validation failed!', next_coord)
                        resolve_AI_state(validationresult)
                    continue

            result = shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode, coordinates=next_coord)
            if type(result) == tuple:  # we have a hit, function returned tuple
                AI_hitcounter += 1
                AI_state = "MULTIPLE_HITS"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2
            else:  # we have a miss, job done, back to random shooting!
                AI_state = "RANDOM"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2

        if AI_state == "RANDOM" and playertogo == 1:
            result = shootingprocess(GRIDSIZE, grid2, grid2_visible, AImode)
            if type(result) == tuple:  # we have a hit, function returned tuple
                AI_primarypoint = result
                AI_hitcounter += 1
                AI_directionlist = AI_rolldirection()
                AI_direction = AI_directionlist.pop(0)
                AI_makeinstructionlist(AI_primarypoint, AI_direction, 5)
                print("AI has got a hit!")
                AI_state = "FIRST_HIT"
                debug_printAIdata()
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2
            else:
                print("AI missed!")
                bslib.showgrid(GRIDSIZE, grid2_visible)
                playertogo = 2

# -------------------------------------------------------------
    elif playertogo == 1:  # begin player block
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
