import sys
from getkey import getkey

def import_card(file_path: str):
    """Permet l’import d’un fichier de jeu. Cette fonction ouvre le fichier, en extrait le contenu et
    le traite de manière a générer les tétraminos définis ainsi que les dimensions du plateau.Return:
    (tuple(x, y), list(tetramino)) → Tuple contenant les dimensions du plateau (sous forme
    d’un tuple (x, y)), ainsi qu’une liste de tetraminos"""
    with open(file_path, 'r') as file:
        lignes = file.readlines()
    dimensions = tuple(map(int, lignes[0].strip().split(',')))
    tetraminos = []
    for line in lignes[1:]:
        tetramino = []
        data = line.strip().split(';;')
        pos_t = []
        for coord in data[0].split(';'):
            coord_vals = tuple(int(val) for val in coord.strip('()').split(','))
            pos_t.append(coord_vals)
        color = data[1]
        offset = (0, 0)
        tetramino.append(pos_t)
        tetramino.append(color)
        tetramino.append(offset)
        tetraminos.append(tetramino)
    return dimensions, tetraminos


def create_grid(w :int, h: int):
    """Crée une grille de taille (3w+2)×(3h+2) , comprenant les délimitations de la zone centrale."""
    full_w = (3 * w) + 2
    full_h = (3 * h) + 2
    board = []
    for i in range(full_h):
        line = []
        if i < h:
            for j in range(full_w):
                line.append('  ')
            board.append(line)
        elif i == h:
            for l in range(w):
                line.append('  ')
            for k in range(w + 1, 2 * w + 1):
                line.append('--')
            for m in range(2 * w + 1, full_w+1):
                line.append('  ')
            board.append(line)
        elif h < i < 2 * h + 1:
            for j in range(full_w):
                if j == w-1:
                    line.append(' |')
                elif j == 2 * w:
                    line.append('| ')
                else:
                    line.append('  ')
            board.append(line)
        elif i == 2 * h + 1:
            for l in range(w):
                line.append('  ')
            for k in range(w + 1, 2 * w + 1):
                line.append('--')
            for m in range(2 * w + 1, full_w + 1):
                line.append('  ')
            board.append(line)
        elif 2 * h + 1 < i < full_h:
            for j in range(full_w):
                line.append('  ')
            board.append(line)
    return board


grid = create_grid(5, 4)


def print_grid(grid):
    """Affiche la grille de jeu dans la console."""
    for line in grid:
        print(line)


def setup_color(tetraminos: list[tuple, str, tuple]):
    for index, tetramino in enumerate(tetraminos):
        color = tetramino[1]
        color_code = '\x1b[' + str(color) + 'm' + str(index) + '\x1b[0m'

    return color_code


def setup_tetraminos(tetraminos: list[tuple[int,int], str, tuple[int,int]], grid: list[list]):
    w, h = import_card(file_path)
    new_grid = [row[:] for row in grid]
    for index, tetramino in enumerate(tetraminos):
        color = setup_color(tetraminos)
        for coord in tetramino[0]:
            if index == 0:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (0, 0)
            elif index == 1:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (w+1, 0)
            elif index == 2:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (2*w + 2, 0)
            elif index == 3:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (0, h+1)
            elif index == 4:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (2*w+2, h+1)
            elif index == 5:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (0, 2*h+2)
            elif index == 6:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (w+1, 2*h+2)
            elif index == 7:
                grid[coord[0]][coord[1]] = color
                tetramino[2] = (2*w+2, 2*h+2)
    return grid, tetraminos




'''
    def place_tetraminos(tetraminos: list(tetramino), grid: list(list)):

    def rotate_tetramino(tetramino: tetramino, clockwise: bool (default=True)):

    def check_move(tetramino: tetramino, grid: list(list)):

    def  check_win(grid: list(list)):'''



