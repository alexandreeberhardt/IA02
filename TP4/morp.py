
"""pour le type de strategie et le random.choice() pour jouer au hasard"""
from typing import Callable
import random

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


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    "transforme un tuple en liste"
    out = []
    for i in grid:
        l = []
        for j in i:
            l.append(j)
        out.append(l)
    return out


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    "transforme une liste en tuple"

    out = (
        (grid[0][0], grid[0][1], grid[0][2]),
        (grid[1][0], grid[1][1], grid[1][2]),
        (grid[2][0], grid[2][1], grid[2][2]),
    )
    return out


def ligne(grid: State, player: Player) -> bool:
    "dis si une ligne est gagnante"

    for i in range(3):
        if grid[i][0] == player and grid[i][1] == player and grid[i][2] == player:
            return True
    return False


def colonne(grid: State, player: Player) -> bool:
    "dis si une colonne est gagnante"

    for i in range(3):
        if grid[0][i] == player and grid[1][i] == player and grid[2][i] == player:
            return True
    return False


def diag(grid: State, player: Player) -> bool:
    "dis si une diagonale est gagnante"
    a=grid[0][0] == player and grid[1][1] == player and grid[2][2] == player
    b=grid[0][2] == player and grid[1][1] == player and grid[2][0] == player
    return a or b



def line(grid: State, player: Player) -> bool:
    "dis si une ligne, colonne ou diagonale est gagnante"

    return ligne(grid, player) or colonne(grid, player) or diag(grid, player)


def plein(grid: State) -> bool:
    "dis si la grille est pleine"
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                return False
    return True


def final(grid: State) -> bool:
    "dis si la partie est terminée"
    return line(grid, 1) or line(grid, 2) or plein(grid)


def score(grid: State) -> float:
    "donne un score d'une grille : 1 si joueur 1, -1 si joueur 2, 0 si nul"
    if line(grid, 1):
        return 1
    if line(grid, 2):
        return -1
    return 0


def pprint(grid: State):
    "affiche proprement une grille"
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 1:
                print("X", end=" ")
            elif grid[i][j] == 2:
                print("O", end=" ")
            else:
                print("0", end=" ")

        print("\n")


def legals(grid: State) -> list[Action]:
    "donne les coup légaux"
    l = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                l.append((i, j))
    return l


def play(grid: State, player: Player, action: Action) -> State:
    "fais jouer un joueur"
    grid = grid_tuple_to_grid_list(grid)
    grid[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(grid)


def strategy(grid: State, player: Player) -> Action:
    "permet au joueur humain de jouer"
    print("à vous de jouer joueur", player)
    print("ligne : ", end="")
    l = int(input())
    print("colonne : ", end="")
    c = int(input())
    if (l, c) not in legals(grid):
        print("coup invalide.")
        print(grid)
        print(legals(grid))
        return strategy(grid, player)
    return (l, c)


def strategy_first_legal(grid: State, player: Player) -> Action:
    "joue le premier coup légal"
    player+=1
    return legals(grid)[0]


def strategy_random(grid: State, player: Player) -> Action:
    "joue un coup au hasard"
    player+=1

    return random.choice(legals(grid))


def tictactoe(strategy_x: Strategy, strategy_o: Strategy, debug: bool = False) -> Score:
    "joue une partie entre 2 statégies"
    if not debug:
        grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        player = 1
        while not final(grid):
            if player == 1:
                print("-------")

                pprint(grid)
                grid = play(grid, 1, strategy_x(grid, 1))
                player = 2
            else:
                print("-------")
                pprint(grid)
                grid = play(grid, 2, strategy_o(grid, 2))
                player = 1
        print("le gagnant est joueur", -score(grid) / 2 + 1.5)
        pprint(grid)
        return score(grid)
    return score(grid)

def minmax(grid: State, player: Player) -> float :
    #Minmax

    if final(grid) :
        return score(grid)

    if player == X : #max player
        bestValue = float('-inf')

        for child in legals(grid) :
            value = minmax(play(grid, X, child), O)
            bestValue = min(bestValue, value)
        return bestValue
    else : #min player
        bestValue = float('inf')

        for child in legals(grid) :
            value = minmax(play(grid, O, child), X)
            bestValue = min(bestValue, value)
        return bestValue
    
def minmaxAction(grid : State, player : Player) -> tuple[float, Action] :
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
            evalScore = minmax(play(grid, X, possibleAction), X)
                    
            if bestScore < evalScore :
                bestScore = evalScore
                bestAction = possibleAction
                
        return bestScore, bestAction

def main():
    "main"
    # print(grid_tuple_to_grid_list(((1,2,3),(4,5,6),(7,8,9))))
    # print(grid_list_to_grid_tuple([[1,2,1],[1,0,1],[2,2,0]]))
    grid=[[2,0,1],[0,0,1],[0,2,0]]
    pprint(grid)
    # print(final(grid))
    # print(legals(grid))
    # pprint(play(grid,2,strategy(grid,2)))
    # print(strategy_first_legal(grid,2))
    #tictactoe(strategy, strategy_random)
    print(minmax(grid,O))


if __name__ == "__main__":
    main()
