from bytestream import *

class HuffmanTree:
    """
    Classe représentant un nœud dans un arbre de Huffman.
    """
    def __init__(self, freq=0, char=None, left=None, right=None):
        """
        Initialise un nœud de l'arbre de Huffman.
        
        Args:
            freq (int): La fréquence du caractère ou la somme des fréquences des nœuds enfants
            char (str, optional): Le caractère associé à ce nœud (uniquement pour les feuilles)
            left (HuffmanTree, optional): Le nœud enfant gauche
            right (HuffmanTree, optional): Le nœud enfant droit
        """
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def is_leaf(self):
        """
        Vérifie si le nœud est une feuille.
        
        Returns:
            bool: True si le nœud est une feuille, False sinon
        """
        return self.left is None and self.right is None
    
    def __repr__(self):
        # N'hésitez pas à modifier cette fonction
        return f"({self.char}:{self.freq})"


def build_freqs(text: str) -> dict[str, int]:
    """
    Construit un dictionnaire de fréquences pour chaque caractère dans le texte.
    
    Args:
        text (str): Le texte à analyser
        
    Returns:
        dict[str, int]: Un dictionnaire associant chaque caractère à sa fréquence
    """
    freqs = {}
    for char in text:
        if char in freqs:
            freqs[char] += 1
        else:
            freqs[char] = 1
    return freqs


def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
    """
    Construit un arbre de Huffman à partir d'un dictionnaire de fréquences.
    
    Args:
        freqs (dict[str, int]): Un dictionnaire associant chaque caractère à sa fréquence
        
    Returns:
        HuffmanTree: La racine de l'arbre de Huffman
    """
    # Créer une liste de nœuds feuilles
    nodes = []
    for char, freq in freqs.items():
        nodes.append(HuffmanTree(freq, char))
    
    # Cas spécial: un seul caractère unique
    if len(nodes) == 1:
        return HuffmanTree(nodes[0].freq, None, nodes[0], HuffmanTree(0))
    
    # Construire l'arbre en fusionnant les nœuds de plus faible fréquence
    while len(nodes) > 1:
        # Trier les nœuds par fréquence
        nodes.sort(key=lambda x: x.freq)
        
        # Prendre les deux nœuds de plus faible fréquence
        left = nodes.pop(0)
        right = nodes.pop(0)
        
        # Créer un nouveau nœud parent
        parent = HuffmanTree(left.freq + right.freq, None, left, right)
        
        # Ajouter le nouveau nœud à la liste
        nodes.append(parent)
    
    # Le dernier nœud est la racine de l'arbre
    return nodes[0]


def build_encodings(tree: HuffmanTree) -> dict[str, str]:
    """
    Construit un dictionnaire d'encodage à partir d'un arbre de Huffman.
    
    Args:
        tree (HuffmanTree): La racine de l'arbre de Huffman
        
    Returns:
        dict[str, str]: Un dictionnaire associant chaque caractère à son code binaire
    """
    encodings = {}
    
    def traverse(node, code):
        if node.is_leaf():
            encodings[node.char] = code
        else:
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")
    
    # Commencer le parcours à partir de la racine avec un code vide
    traverse(tree, "")
    
    return encodings


def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
    """
    Encode une chaîne de caractères en utilisant l'arbre de Huffman.
    
    Args:
        plain (str): La chaîne à encoder
        tree (HuffmanTree): La racine de l'arbre de Huffman
        
    Returns:
        bytes: La chaîne encodée sous forme de bytes
    """
    from bytestream import bin2bytes
    
    # Construire le dictionnaire d'encodage
    encodings = build_encodings(tree)
    
    # Encoder chaque caractère
    binary = ""
    for char in plain:
        binary += encodings[char]
    
    # Convertir la chaîne binaire en bytes
    return bin2bytes(binary)


def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
    """
    Décode une chaîne de bytes en utilisant l'arbre de Huffman.
    
    Args:
        bytestream (bytes): La chaîne encodée sous forme de bytes
        tree (HuffmanTree): La racine de l'arbre de Huffman
        
    Returns:
        str: La chaîne décodée
    """
    from bytestream import bytes2bin
    
    # Convertir les bytes en chaîne binaire
    binary = bytes2bin(bytestream)
    
    # Décoder la chaîne binaire
    result = ""
    current_node = tree
    
    for bit in binary:
        # Naviguer dans l'arbre selon le bit
        if bit == "0":
            current_node = current_node.left
        else:  # bit == "1"
            current_node = current_node.right
        
        # Si on atteint une feuille, ajouter le caractère au résultat et revenir à la racine
        if current_node.is_leaf():
            result += current_node.char
            current_node = tree
    
    return result
