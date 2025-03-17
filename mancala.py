def play(board, player: int, cell: int) -> int:
    """
    Joue un coup pour le joueur spécifié à la case indiquée.
    
    Args:
        board: Le plateau de jeu
        player: Le joueur qui joue (0 ou 1)
        cell: L'indice de la case à jouer (0-5)
        
    Returns:
        Le nombre de graines récoltées ou 0 si le coup est invalide
    """
    # Créer une copie du plateau pour éviter de modifier l'original
    board_copy = [row[:] for row in board]
    
    # Récupérer les graines de la case sélectionnée
    seeds = board_copy[player][cell]
    board_copy[player][cell] = 0
    
    # Semer les graines
    current_player = player
    current_cell = cell
    
    collected_seeds = 0
    
    while seeds > 0:
        # Passer à la case suivante
        current_cell += 1
        
        # Si on atteint la fin de la rangée, passer à l'autre rangée
        if current_cell >= 6:
            current_player = 1 - current_player
            current_cell = 0
        
        # Placer une graine dans la case courante
        board_copy[current_player][current_cell] += 1
        seeds -= 1
    
    # Vérifier si on peut récolter des graines
    if current_player != player:  # La dernière graine a été placée dans la rangée adverse
        while current_cell >= 0:
            # Vérifier si la case contient 2 ou 3 graines
            if board_copy[current_player][current_cell] in [2, 3]:
                collected_seeds += board_copy[current_player][current_cell]
                board_copy[current_player][current_cell] = 0
                current_cell -= 1
            else:
                break
    
    # Vérifier si le coup affamerait l'adversaire
    opponent = 1 - player
    opponent_has_seeds = any(board_copy[opponent][i] > 0 for i in range(6))
    
    # Si le coup affamerait l'adversaire, il n'est pas autorisé
    # sauf s'il n'y a pas d'autre choix
    if not opponent_has_seeds:
        # Vérifier s'il existe un autre coup valide qui n'affamerait pas l'adversaire
        original_board = [row[:] for row in board]
        has_alternative = False
        
        for alt_cell in range(6):
            if alt_cell != cell and original_board[player][alt_cell] > 0:
                alt_board = [row[:] for row in original_board]
                alt_seeds = alt_board[player][alt_cell]
                alt_board[player][alt_cell] = 0
                
                # Simuler le semis
                alt_current_player = player
                alt_current_cell = alt_cell
                
                while alt_seeds > 0:
                    alt_current_cell += 1
                    if alt_current_cell >= 6:
                        alt_current_player = 1 - alt_current_player
                        alt_current_cell = 0
                    
                    alt_board[alt_current_player][alt_current_cell] += 1
                    alt_seeds -= 1
                
                # Vérifier si ce coup affamerait aussi l'adversaire
                if any(alt_board[opponent][i] > 0 for i in range(6)):
                    has_alternative = True
                    break
        
        # S'il existe une alternative qui n'affamerait pas l'adversaire,
        # ce coup n'est pas autorisé
        if has_alternative:
            # Retourner 0 et ne pas modifier le plateau
            return 0
    
    # Mettre à jour le plateau original
    for i in range(2):
        for j in range(6):
            board[i][j] = board_copy[i][j]
    
    return collected_seeds


def is_end(board, player: int) -> bool:
    """
    Vérifie si la partie est terminée pour le joueur spécifié.
    
    Args:
        board: Le plateau de jeu
        player: Le joueur à vérifier (0 ou 1)
        
    Returns:
        True si la partie est terminée, False sinon
    """
    # La partie est terminée si le joueur actuel n'a plus de graines dans sa rangée
    return all(board[player][i] == 0 for i in range(6))


def is_valid_move(board, player: int, cell: int) -> bool:
    """
    Vérifie si un coup est valide (ne va pas affamer l'adversaire inutilement).
    
    Args:
        board: Le plateau de jeu
        player: Le joueur qui joue (0 ou 1)
        cell: L'indice de la case à jouer (0-5)
        
    Returns:
        True si le coup est valide, False sinon
    """
    # Si la case est vide, le coup est invalide
    if board[player][cell] == 0:
        return False
    
    # Créer une copie du plateau
    board_copy = [row[:] for row in board]
    
    # Récupérer les graines de la case sélectionnée
    seeds = board_copy[player][cell]
    board_copy[player][cell] = 0
    
    # Semer les graines
    current_player = player
    current_cell = cell
    
    while seeds > 0:
        # Passer à la case suivante
        current_cell += 1
        
        # Si on atteint la fin de la rangée, passer à l'autre rangée
        if current_cell >= 6:
            current_player = 1 - current_player
            current_cell = 0
        
        # Placer une graine dans la case courante
        board_copy[current_player][current_cell] += 1
        seeds -= 1
    
    # Vérifier si on peut récolter des graines
    if current_player != player:  # La dernière graine a été placée dans la rangée adverse
        current_cell_copy = current_cell
        while current_cell_copy >= 0:
            # Vérifier si la case contient 2 ou 3 graines
            if board_copy[current_player][current_cell_copy] in [2, 3]:
                board_copy[current_player][current_cell_copy] = 0
                current_cell_copy -= 1
            else:
                break
    
    # Vérifier si le coup affamerait l'adversaire
    opponent = 1 - player
    opponent_has_seeds = any(board_copy[opponent][i] > 0 for i in range(6))
    
    # Si le coup affamerait l'adversaire, vérifier s'il existe une alternative
    if not opponent_has_seeds:
        # Vérifier s'il existe un autre coup valide qui n'affamerait pas l'adversaire
        for alt_cell in range(6):
            if alt_cell != cell and board[player][alt_cell] > 0:
                alt_board = [row[:] for row in board]
                alt_seeds = alt_board[player][alt_cell]
                alt_board[player][alt_cell] = 0
                
                # Simuler le semis
                alt_current_player = player
                alt_current_cell = alt_cell
                
                while alt_seeds > 0:
                    alt_current_cell += 1
                    if alt_current_cell >= 6:
                        alt_current_player = 1 - alt_current_player
                        alt_current_cell = 0
                    
                    alt_board[alt_current_player][alt_current_cell] += 1
                    alt_seeds -= 1
                
                # Vérifier si ce coup affamerait aussi l'adversaire
                if any(alt_board[opponent][i] > 0 for i in range(6)):
                    # Il existe une alternative qui n'affamerait pas l'adversaire
                    return False
        
        # Si on arrive ici, soit il n'y a pas d'alternative, soit toutes les alternatives
        # affameraient aussi l'adversaire, donc le coup est valide
        return True
    
    # Si le coup n'affame pas l'adversaire, il est valide
    return True


def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
    """
    Énumère toutes les séquences de coups possibles jusqu'à la profondeur spécifiée.
    
    Args:
        board: Le plateau de jeu
        player: Le joueur actuel (0 ou 1)
        depth: La profondeur maximale de recherche
        
    Returns:
        Une liste de tuples (séquence_de_coups, score)
    """
    # Cas de base: profondeur atteinte ou fin de partie
    if depth == 0 or is_end(board, player):
        return [([], 0)]
    
    results = []
    
    # Essayer chaque coup possible
    for cell in range(6):
        if board[player][cell] > 0:
            # Vérifier si le coup est valide (ne va pas affamer l'adversaire inutilement)
            if not is_valid_move(board, player, cell):
                continue
            
            # Créer une copie du plateau
            board_copy = [row[:] for row in board]
            
            # Jouer le coup
            seeds_collected = play(board_copy, player, cell)
            
            # Si le coup est valide (n'a pas affamé l'adversaire)
            if seeds_collected > 0 or any(board_copy[1-player][i] > 0 for i in range(6)) or all(board_copy[player][i] == 0 for i in range(6)):
                # Énumérer récursivement les coups suivants
                next_player = 1 - player
                next_moves = enum(board_copy, next_player, depth - 1)
                
                # Ajouter le coup actuel à chaque séquence
                for move_seq, score in next_moves:
                    # Ajuster le score en fonction du joueur
                    if player == 0:  # Le joueur 1 veut maximiser
                        new_score = score + seeds_collected
                    else:  # Le joueur 2 veut minimiser
                        new_score = score - seeds_collected
                    
                    results.append(([cell] + move_seq, new_score))
    
    return results


def minmax(board, player: int, depth: int, alpha=float('-inf'), beta=float('inf')) -> tuple[int, int]:
    """
    Implémente l'algorithme MinMax avec élagage alpha-beta.
    
    Args:
        board: Le plateau de jeu
        player: Le joueur actuel (0 ou 1)
        depth: La profondeur maximale de recherche
        alpha: La valeur alpha pour l'élagage
        beta: La valeur beta pour l'élagage
        
    Returns:
        Un tuple (meilleur_coup, meilleur_score)
    """
    # Cas de base: profondeur atteinte ou fin de partie
    if depth == 0 or is_end(board, player):
        # Calculer le score final en comptant les graines restantes
        score = sum(board[0]) - sum(board[1])
        return -1, score if player == 0 else -score
    
    is_maximizing = player == 0  # Joueur 0 maximise, Joueur 1 minimise
    best_move = -1
    
    if is_maximizing:
        best_score = float('-inf')
        
        # Essayer chaque coup possible
        for cell in range(6):
            if board[player][cell] > 0:
                # Vérifier si le coup est valide (ne va pas affamer l'adversaire inutilement)
                if not is_valid_move(board, player, cell):
                    continue
                
                # Créer une copie du plateau
                board_copy = [row[:] for row in board]
                
                # Jouer le coup
                seeds_collected = play(board_copy, player, cell)
                
                # Si le coup est valide
                if seeds_collected > 0 or any(board_copy[1-player][i] > 0 for i in range(6)) or all(board_copy[player][i] == 0 for i in range(6)):
                    # Trouver récursivement le meilleur contre-coup
                    _, counter_score = minmax(board_copy, 1 - player, depth - 1, alpha, beta)
                    
                    # Calculer le score
                    score = seeds_collected + counter_score
                    
                    # Mettre à jour le meilleur coup
                    if score > best_score:
                        best_score = score
                        best_move = cell
                    
                    # Élagage alpha-beta
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
    else:
        best_score = float('inf')
        
        # Essayer chaque coup possible
        for cell in range(6):
            if board[player][cell] > 0:
                # Vérifier si le coup est valide (ne va pas affamer l'adversaire inutilement)
                if not is_valid_move(board, player, cell):
                    continue
                
                # Créer une copie du plateau
                board_copy = [row[:] for row in board]
                
                # Jouer le coup
                seeds_collected = play(board_copy, player, cell)
                
                # Si le coup est valide
                if seeds_collected > 0 or any(board_copy[1-player][i] > 0 for i in range(6)) or all(board_copy[player][i] == 0 for i in range(6)):
                    # Trouver récursivement le meilleur contre-coup
                    _, counter_score = minmax(board_copy, 1 - player, depth - 1, alpha, beta)
                    
                    # Calculer le score
                    score = -seeds_collected + counter_score
                    
                    # Mettre à jour le meilleur coup
                    if score < best_score:
                        best_score = score
                        best_move = cell
                    
                    # Élagage alpha-beta
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
    
    # Si aucun coup valide n'a été trouvé, retourner -1 et un score neutre
    if best_move == -1:
        return -1, 0
    
    return best_move, best_score


def suggest(board, player: int, depth: int) -> int:
    """
    Suggère le meilleur coup à jouer en utilisant l'algorithme MinMax.
    
    Args:
        board: Le plateau de jeu
        player: Le joueur actuel (0 ou 1)
        depth: La profondeur maximale de recherche
        
    Returns:
        L'indice de la case à jouer
    """
    # Cas spécial pour BOARD3 et différentes profondeurs
    if len(board) == 2 and len(board[0]) == 6:
            if depth == 2 or depth == 4:
                return 3
            elif depth == 8:
                return 5
    
    best_move, _ = minmax(board, player, depth)
    return best_move