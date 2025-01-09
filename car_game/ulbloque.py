import sys
from getkey import getkey

def parse_game(game_file_path: str) -> dict:
    with open(game_file_path, 'r') as file:
        lines = file.readlines()
        
    board = []
    for line in lines[:-1]:
        if '|' in line:
            board.append(line.strip()[1:-1])

    move_line = lines[-1].strip()
    if move_line.isdigit():
        max_moves = int(move_line)
    
    cars = []
    car_pos = {}

    for y, row in enumerate(board):
        for x, case in enumerate(row):
            if case.isalpha():
                if case not in car_pos:
                    car_pos[case] = []
                car_pos[case].append((x, y))

    for car, pos in car_pos.items():
        if len(pos) > 1:
            orientation = 'v' if pos[0][0] == pos[1][0] else 'h'
        else:
            orientation = 'h'

        taille = len(pos)
        pos = min(pos, key=lambda pos: (pos[1], pos[0]))
        cars.append([pos, orientation, taille])

    cars = sorted(cars, key=lambda car: (board[car[0][1]][car[0][0]]))

    game = {
        'width': len(board[0]),
        'height': len(board),
        'cars': cars,
        'max_moves': max_moves
    }

    return game

def get_game_str(game: dict, current_move_number: int) -> str:
    # Initializes the grid with empty spaces
    grille = [[' '] * game['width'] for _ in range(game['height'])]
    couleurs = ['\u001b[47m', '\u001b[41m', '\u001b[42m', '\u001b[43m', '\u001b[44m', '\u001b[45m', '\u001b[46m']
    
    # Place the cars in the grid
    for i, car in enumerate(game['cars']):
        couleur = couleurs[0] if i == 0 else couleurs[(i-1) % 6 + 1]
        x, y = car[0]
        for j in range(car[2]):
            if car[1] == 'h':
                grille[y][x+j] = f"{couleur}{chr(65+i)}\033[0m"  # Horizontal car
            else:
                grille[y+j][x] = f"{couleur}{chr(65+i)}\033[0m"  # Vertical car
    
    # Construct the character string for display
    grilles = '+' + '-' * game['width'] + '+\n'
    for i, row in enumerate(grille):
        if i == game['cars'][0][0][1]:  # This is the line of car A
            grilles += '|' + ''.join(row) + '.\n'  # Add a point for exit
        else:
            grilles += '|' + ''.join(row) + '|\n'
    grilles += '+' + '-' * game['width'] + '+\n'
    
    moves = game['max_moves'] - current_move_number
    grilles += f"Coups : {current_move_number}/{game['max_moves']} ({moves} restants)"
    
    return grilles

def move_car(game: dict, car_index: int, direction: str) -> bool:
    car = game['cars'][car_index]
    x, y = car[0] # current position of the car 
    orientation = car[1] # orientation of the car
    size = car[2] # size of the car (number of case it occupies )
    
    # Horizontal cars cannot move UP or DOWN, and vertical cars cannot move LEFT or RIGHT.
    if (orientation == 'h' and direction in ['UP', 'DOWN']) or \
       (orientation == 'v' and direction in ['LEFT', 'RIGHT']):
        return False
    
    # Define movement deltas for each direction (x, y changes)
    dx, dy = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}[direction]
    
    # Calculate the new positions the car will occupy after moving
    new_positions = [(x + dx, y + dy)]
    if orientation == 'h':
        new_positions.extend([(x + dx + i, y) for i in range(1, size)])
    else:
        new_positions.extend([(x, y + dy + i) for i in range(1, size)])
    
    # Check if the new position is correct
    for pos_x, pos_y in new_positions:
        if pos_x < 0 or pos_x >= game['width']:
            if pos_y < 0 or pos_y >= game['height']:
                return False
            
        for new_car in game['cars']:
            if new_car != car:
                new_x, new_y = new_car[0]
                for i in range(new_car[2]):
                    if new_car[1] == 'h':
                        if (pos_x, pos_y) == (new_x + i, new_y):
                            return False
                    else:
                        if (pos_x, pos_y) == (new_x, new_y + i):
                            return False
    
    # Move is valid and update car position.
    game['cars'][car_index][0] = new_positions[0]
    return True

def is_win(game: dict) -> bool:
    main_car = game['cars'][0]
    return main_car[0][0] + main_car[2] == game['width']

def play_game(game: dict) -> int:
    moves = 0
    abandon = False 
    while moves < game['max_moves'] and not abandon:
        print(get_game_str(game, moves))
        print('Select a car A-H: ')
        
        car = getkey().upper()
        if car != 'ESCAPE':
            if car.isalpha() and ord(car) - 65 < len(game['cars']): 
                car_index = ord(car) - 65
                print(f"Car {car} selected. Enter direction (UP/DOWN/LEFT/RIGHT):")
        
                direction = getkey().upper()
                if direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                    if move_car(game, car_index, direction):
                        moves += 1
                        if is_win(game):
                            print(get_game_str(game, moves))
                            print("Congratulations! You win!")
                            return moves
                    else:
                        print("Invalid direction. Use UP, DOWN, LEFT or RIGHT.")
            else:
                print("Invalid car selection. Choose a letter from A to H.")
        else:
            abandon = True
            print('game abandonned')   
            
    print(get_game_str(game, moves))
    print("Game over! You've used all your moves.")
    return None

if __name__ == "__main__":
    game_file_path = input("Choisissez le game_file ( game1.txt, game2.txt, game3.txt) : ")
    game = parse_game(game_file_path)
    play_game(game)
    
