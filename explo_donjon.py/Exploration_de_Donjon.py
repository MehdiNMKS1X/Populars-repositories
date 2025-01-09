import random

# Initialisation du seed pour la génération aléatoire
random.seed(10)

def lire_carte(fichier: str) -> dict:
    """
    Ouvre et lit le fichier vers le chemin reçu en paramètre
    Récupère dans le dictionnaire la taille du donjon et les positions des monstres regroupées par leur symbole
    """
    carte = {"taille": 0, "monstres": {}}
    with open(fichier, 'r') as f:
        taille_ligne = f.readline().strip()
        partis = taille_ligne.split(':')
        carte['taille'] = int(partis[1].strip())
    
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                parties = ligne.split(':')
                monstres, position= parties
                monstre = monstres.split()[-1]
            
                carte['monstres'][monstre]= []
                for pos in position.split(';'):
                    coords = pos.strip().split(',')
                    x, y = int(coords[0]), int(coords[1])
                    carte['monstres'][monstre].append((x, y))
    return carte


def grille_string(grille) -> str:
    """
    Renvoie une représentation de la grille sous forme de string
    """
    bordure =' -' * (len(grille)*2 - 4)
    return bordure + ' \n' + ' \n'.join('| ' + '  '.join(ligne) + '  |' for ligne in grille) + ' \n' + bordure

def afficher_grille(grille, vie: int, tresors_restants: int) -> None:
    """
    Affiche la grille et le résultat points de vie et trésor(s) restant(s)
    """
    print()
    print(grille_string(grille))
    print(f"Points de vie : {vie}")
    print(f"Trésor(s) restant(s) : {tresors_restants}")

def deplacer_personnage(direction, position_personnage, grille, vie) -> tuple:
    """
    Déplace le joueur sur la carte et renvoie un tuple driection,position_personnage, grille, vie
    """
    x, y = position_personnage
    dx, dy = {"h": (-1, 0), "b": (1, 0), "g": (0, -1), "d": (0, 1)}[direction]
    nx, ny = x + dx, y + dy
    
    if 0 <= nx < len(grille) and 0 <= ny < len(grille[0]):
        grille[x][y] = '*'
        if grille[nx][ny] in 'ABCDEFGHIJ':
            vie -= 3 * (ord(grille[nx][ny]) - ord('A') + 1)
        grille[nx][ny] = 'P'
        return ((nx, ny), grille, vie)
    
    return (position_personnage, grille, vie)

def initialise_jeu(carte: dict, difficulte: int) -> tuple:
    """
    Initialise le jeu en fonction de la difficulté choisi
    """
    taille = carte["taille"]
    grille = [['*' for _ in range(taille)] for _ in range(taille)]
    
    # Place les monstres
    for monstre, positions in carte["monstres"].items():
        for x, y in positions:
            grille[x][y] = monstre
    
    # Place le personnage
    grille[0][0] = 'P'
    position_personnage = (0, 0)
    
    # Initialise les points de vie et les trésors en fonction de la difficulté
    if difficulte == 0:
        vie = 100
        tresors = 3
    elif difficulte == 1:
        vie = 20
        tresors = 6
    else:
        vie = 10
        tresors = 10
    
    # Place les trésors
    tresors_places = 0
    while tresors_places < tresors:
        x, y = random.randint(0, taille-1), random.randint(0, taille-1)
        if grille[x][y] == '*':
            grille[x][y] = 'T' if difficulte == 0 else '*'
            tresors_places += 1
    
    return grille, position_personnage, vie, tresors

def play():
    """
    Fonction principale pour jouer au jeu
    """
    carte = lire_carte("carte.txt")
    difficulte = int(input("Choisissez la difficulté (0: Facile, 1: Moyen, 2: Difficile) : "))
    grille, position_personnage, vie, tresors_restants = initialise_jeu(carte, difficulte)
    
    while vie > 0 and tresors_restants > 0:
        afficher_grille(grille, vie, tresors_restants)
        direction = input("Entrez une direction (h/b/g/d) : ")
        while direction not in 'hbgd':
            direction = input("Seulement 4 déplacements possible! Entrez: h: haut, b: bas, g: gauche, d: droite : ")
        
        position_personnage, grille, vie = deplacer_personnage(direction, position_personnage, grille, vie)
        
        # Vérifie si un trésor a été trouvé
        x, y = position_personnage
        if grille[x][y] == 'T':
            tresors_restants -= 1
            grille[x][y] = 'P'
    
    if vie <= 0:
        print("Vous êtes mort... Game over !")
    else:
        print("Félicitations, vous avez collecté tous les trésors !")

if __name__ == "__main__":
    play()