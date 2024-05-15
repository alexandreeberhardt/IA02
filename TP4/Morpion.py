import random
from typing import Callable, List, Tuple

# Quelques structures de données

Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[Grid, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2

# Functions

def gridTupleToGridList(grid: Grid) -> list[list[int]] :
    #Tuple to List[list]
    listOut = []
    for tuple in grid :
        listEl = []
        for element in tuple :
            listEl.append(element)
        listOut.append(listEl)
    return listOut


def gridListToGridTuple(grid: list[list[int]]) -> Grid :
    #List[List] to Tuple
    listTuple = []
    for listInt in grid :
        listTuple.append(tuple(listInt))
    tupleOut = tuple(listTuple)
    return tupleOut

def rows(grid: State, player: Player) -> bool :
    #Check grid's rows
    if (
        (grid[0][0] == player and grid[0][1] == player and grid[0][2] == player)
        or 
        (grid[1][0] == player and grid[1][1] == player and grid[1][2] == player)
        or 
        (grid[2][0] == player and grid[2][1] == player and grid[2][2] == player)
    ) :
        return True
    return False

def column(grid: State, player: Player) -> bool :
    #Check grid's columns
    if (
        (grid[0][0] == player and grid[1][0] == player and grid[2][0] == player)
        or 
        (grid[0][1] == player and grid[1][1] == player and grid[2][1] == player)
        or 
        (grid[0][2] == player and grid[1][2] == player and grid[2][2] == player)
    ) :
        return True
    return False

def diag(grid: State, player: Player) -> bool :
    #Check grid's diags
    if (grid[0][0] == player and grid[1][1] == player and grid[2][2] == player) or (grid[0][2] == player and grid[1][1] == player and grid[2][0] == player) :
        return True
    return False

def line(grid: State, player: Player) -> bool :
    # Check grid's lines
    if (rows(grid, player) or column(grid, player) or diag(grid, player)) :
        return True
    return False

def isGridFull(grid : State) -> bool :
    for line in grid :
        for element in line :
            if element == 0 : #possibility to play 
                return False
    return True

def final(grid: State) -> bool :
    #Check final state
    if line(grid, X) or line(grid, O) or isGridFull(grid) :
        return True
    return False

def score(grid: State) -> float :
    #Return score
    if line(grid, X) :
        return 1
    if line(grid, O) :
        return -1
    if isGridFull(grid) :
        return 0

def pprint(grid: State) :
    #Prints game
    for line in grid :
        for element in line :
            if (element == 1) :
                print("X", end = "  ")
            else :
                if (element == 2) :
                    print("O", end = "  ")
                else :
                    print(element, end = "  ")
        print("")

def legals(grid: State) -> list[Action] :
    #Returns available actions for a chosen player
    listLegals = []
    for row in range(len(grid[0])) :
        for col in range(len(grid[0])) :
            if grid[row][col] == 0 :
                listLegals.append(((row, col)))
    return listLegals

def play(grid: State, player: Player, action: Action) -> State :
    #Updates game
    gridList = gridTupleToGridList(grid)
    gridList[action[0]][action[1]] = player
    return gridListToGridTuple(gridList)
    
def strategy(grid: State, player: Player) -> Action :
    #Default playing strategy
    selection = False
    actions = legals(grid)
    print ("Available actions :")
    for action in actions :
        print(action)

    while not selection :
        row = int(input("Select a row :"))
        col = int(input("Select a col :"))
        for action in actions :
            if (row, col) == action :
                selection = True
                return action
    
def strategy_first_legal(grid: State, player: Player) -> Action :
    #First action strategy
    return legals(grid)[0]

def strategy_random(grid: State, player: Player) -> Action :
    #Random choice strategy
    return random.choice(legals(grid))
    
def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score :
    #Gameplay
    grid = (
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0)
    )

    while not final(grid) :
        pprint(grid)
        print("")
        actionX = strategy_X(grid, X)
        grid = play(grid, X, actionX)
        if final(grid) :
            break
        pprint(grid)
        print("")
        actionO = strategy_O(grid, O)
        grid = play(grid, O, actionO)

    pprint(grid)
    return score(grid)

def minmax(grid: State, player: Player) -> float :
    #Minmax

    if final(grid) :
        return score(grid)

    if player == X : #max player
        bestValue = float('-inf')

        for child in legals(grid) :
            value = minmax(play(grid, X, child), O)
            bestValue = max(bestValue, value)
        return bestValue
    
    else : #min player
        bestValue = float('inf')

        for child in legals(grid) :
            value = minmax(play(grid, O, child), X)
            bestValue = min(bestValue, value)
        return bestValue
    
def minmaxAction(grid : State, player : Player, depth : int = 0) -> tuple[float, Action] :
    #bestAction MinMax
    if player == X : #max player
        bestScore = float ('-inf')

        for possibleAction in legals(grid) :
            evalScore = minmax(play(grid, X, possibleAction), O)

            if bestScore < evalScore :
                bestScore = evalScore
                bestAction = possibleAction
        
        return bestScore, bestAction
    
    else : #min player
        bestScore = float('inf')
        for possibleAction in legals(grid) :
            evalScore = minmax(play(grid, O, possibleAction), X) 

            if bestScore > evalScore :
                bestScore = evalScore
                bestAction = possibleAction
                
        return bestScore, bestAction

def strategyMinmax(grid: State, player: Player) -> Action :
    #returns action from Minmax
    return minmaxAction(grid, player)[1]

def minmaxActions(grid: State, player: Player, depth: int = 0) -> tuple[float, list[Action]] :
    #returns list of all minMax Actions for optimal score
    listActions = []
    score = 0

    while not(final(grid)) :
        result = strategyMinmax(grid, player)
        score = result[0]
        listActions.append(result[1])
        grid = play(grid, player, result[1])
    
    return score, listActions

def strategy_minmaxRandom(grid: State, player: Player) -> Action :
    return random.choice(minmaxActions(grid, player)[1])

def alphaBeta(grid: State, alpha : float, beta : float, player: Player) -> float :
    #alphaBeta
    if final(grid) :
        return score(grid)

    if player == X : #max player
        value = float('-inf')

        for child in legals(grid) :
            value = max(value, alphaBeta(play(grid, X, child), alpha, beta, O))
            alpha = max(alpha, value)

            if alpha >= beta :
                break
        return value

    else : #min player
        value = float('inf')

        for child in legals(grid) :
            value = max(value, alphaBeta(play(grid, O, child), alpha, beta, X))
            beta = min(beta, value)
            if alpha >= beta :
                break
        return value
    
def alphaBetaAction(grid : State, player : Player, depth : int = 0) -> tuple[float, Action] :
    #bestAction MinMax
    if player == X : #max player
        bestScore = float ('-inf')

        for possibleAction in legals(grid) :
            evalScore = alphaBeta(play(grid, X, possibleAction), '-inf', 'inf', O)
            
            if bestScore < evalScore :
                bestScore = evalScore
                bestAction = possibleAction
        
        return bestScore, bestAction
    
    else : #min player
        bestScore = float('inf')
        for possibleAction in legals(grid) :
            evalScore = alphaBeta(play(grid, O, possibleAction), '-inf', 'inf', X) 
            if bestScore > evalScore :
                bestScore = evalScore
                bestAction = possibleAction
                
        return bestScore, bestAction

def main() :
    #Main
    score = tictactoe(strategyMinmax, strategy)
    if (score == 1) :
        print ("Le joueur X gagne !")
        return
    if (score == -1) :
        print ("Le joueur 2 gagne !")
        return
    if (score == 0) :
        print ("Match nul ! ")



# Calls
main()

