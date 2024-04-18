"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.0
"""

from typing import List, Tuple
import subprocess
#import pprint
from itertools import combinations

# alias de types
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],    
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]

test: Grid = [
    [0, 9, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 8, 0],
    [0, 5, 4, 0, 3, 0, 7, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 2],
    [0, 7, 3, 0, 5, 0, 8, 0, 0],
    [9, 0, 0, 0, 0, 0, 4, 0, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 4, 6, 0, 0, 5, 0, 1, 0],
]

empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def write_dimacs_file(dimacs: str, filename: str):
    "ajoute les dimacs dans un fichier"
    with open(filename, "w", newline="",encoding="utf8") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    "execute gophersat en revoie true/false et un modele"
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")
    modelint = []
    for i in model:
        modelint.append(int(i))
    afficher_grille(model_to_grid(modelint, 9))

    return True, [int(x) for x in model]


def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    """i la ligne [0;8], j la colonne [0;8] et val la valeur de la variable"""
    return 81 * i + 9 * j + val + 1


def variable_to_cell(var: PropositionnalVariable) -> Tuple[int, int, int]:
    "passe d'une variable à une cellue"
    var -= 1
    ligne = var // 81
    col = var % 81 // 9
    val = var % 9
    return (ligne, col, val)


def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    "passe d'un modele à une grille"
    sudoku = []
    for i in range(nb_vals):
        ligne = []
        for j in range(nb_vals):
            for k in range(nb_vals):
                if model[cell_to_variable(i, j, k - 1)] > 0:
                    ligne.append(
                        (model[cell_to_variable(i, j, k - 1)] - 1) % nb_vals + 1
                    )
        sudoku.append(ligne)
    return sudoku


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    "ajoute les clauses pour avoir au moins une valeur par case"
    liste = []
    for i in variables:
        liste.append(i)
    return liste


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    "ajoute les clauses pour ne pas avoir plusieurs variables d'une meme liste"
    clauses = []
    clauses.append(at_least_one(variables))
    a = combinations(variables, 2)
    for item in a:
        clauses.append([-item[0], -item[1]])
    return clauses


def create_cell_constraints() -> ClauseBase:
    "ajoute les clauses d'une cellule"
    clauses = []
    for i in range(0, 729, 9):
        clauses += unique(
            [1 + i, 2 + i, 3 + i, 4 + i, 5 + i, 6 + i, 7 + i, 8 + i, 9 + i]
        )
    return clauses


def create_line_constraints() -> ClauseBase:
    "ajoute les clauses d'une ligne"
    clauses = []
    for i in range(9):
        for j in range(9):
            liste = []
            for a in range(9):
                liste.append(cell_to_variable(i, a, j))
            clauses.append(at_least_one(liste))
    return clauses


def create_column_constraints() -> ClauseBase:
    "ajoute les clauses d'une colonne"
    clauses = []
    for i in range(9):
        for j in range(9):
            liste = []
            for a in range(9):
                liste.append(cell_to_variable(a, i, j))
            clauses.append(at_least_one(liste))
    return clauses


def create_box_constraints() -> ClauseBase:
    "ajout les clauses d'une box"
    clauses = []
    for i in range(3):
        for j in range(3):
            for z in range(9):
                liste = []
                for x in range(3):
                    for y in range(3):
                        liste.append((3 * j + y) * 9 + (3 * i + x) * 81 + z + 1)
                clauses.append(at_least_one(liste))
    return clauses


def create_value_constraints(grid: Grid) -> ClauseBase:
    "ajoute les clauses des valeurs connues de bases"
    clauses = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                clauses.append([cell_to_variable(i,j,grid[i][j]-1)])
    return clauses


def generate_problem(grid: Grid) -> ClauseBase:
    "genere les clauses completes à partir d'une grille"
    clauses = []
    clauses += create_value_constraints(grid)
    clauses += create_cell_constraints()
    clauses += create_line_constraints()
    clauses += create_column_constraints()
    clauses += create_box_constraints()
    return clauses


def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    "transforme la base de clauses en dimacs"
    chaine = f"p cnf {nb_vars} {len(clauses)} \n"
    for i in clauses:
        for j in i:
            chaine += f"{j} "
        chaine += "0\n"
    return chaine


def afficher_grille(grille: Grid):
    "fonction d'affichage graphique pour que ça soit tout beau"
    print("-------------------------")
    for i, ligne in enumerate(grille):
        if i % 3 == 0 and i != 0:
            print("-------------------------")
        print("|", end=" ")
        for j, valeur in enumerate(ligne):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(valeur, end=" ")
        print("|")
    print("-------------------------")


def main():
    "main"
    # print(cell_to_variable(1,3,4))
    # print(variable_to_cell(cell_to_variable(1,3,4)))
    # pprint.pp(model_to_grid(model,9))
    # print(at_least_one([1, 3, 5]))
    # print(unique([1,3,5]))
    # print(create_cell_constraints())
    # print(create_line_constraints())
    # print(create_column_constraints())
    # print(cell_to_variable(0,0,0))
    # print(create_box_constraints())
    # print(create_value_constraints(example))
    # print(generate_problem(example))
    # print (clauses_to_dimacs([[-1, -2], [1, 2], [1, 3], [2, 4], [-3, 4], [-4, 5]],5))
    # afficher_grille(test)
    # print(cell_to_variable(0,0,0))
    write_dimacs_file(clauses_to_dimacs(generate_problem(test),729),"sudoku.cnf")
    exec_gophersat("sudoku.cnf")


if __name__ == "__main__":
    main()
