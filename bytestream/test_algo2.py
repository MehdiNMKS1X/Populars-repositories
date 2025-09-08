import os
from os import path

from bytestream import bytes2bin
from huffman import huffman_encode, huffman_decode, build_freqs, build_huffman_tree, build_encodings



TEXT1 = "hello-world"
TEXT2 = "to be, or not to be, that is the question"
TEXT3 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce commodo erat vel eros mattis lacinia. Integer euismod diam sit amet mauris feugiat convallis quis sed mi. Duis nibh eros, tristique in maximus quis, ornare vel ex. Ut sed luctus nisi. Etiam mattis eget lorem sit amet congue. Praesent at nulla ac tortor egestas malesuada nec in neque. Maecenas euismod orci vel ante scelerisque vulputate."
FILE4 = "./LICENCE.txt"



def test_freqs_text1():
  freqs = build_freqs(TEXT1)
  expected = {'h': 1, 'e': 1, 'l': 3, 'o': 2, '-': 1, 'w': 1, 'r': 1, 'd': 1}
  assert len(freqs) == len(expected), "Il y a des caractères en trop ou il manque certains caractères"
  assert freqs == expected, "Dictionnaire de fréquences invalide"

def test_freqs_text2():
  freqs = build_freqs(TEXT2)
  expected = {'t': 7, 'o': 5, ' ': 9, 'b': 2, 'e': 4, ',': 2, 'r': 1, 'n': 2, 'h': 2, 'a': 1, 'i': 2, 's': 2, 'q': 1, 'u': 1}
  assert len(freqs) == len(expected), "Il y a des caractères en trop ou il manque certains caractères"
  assert freqs == expected, "Dictionnaire de fréquences invalide"

def test_freqs_text3():
  freqs = build_freqs(TEXT3)
  expected = {'L': 1, 'o': 18, 'r': 17, 'e': 43, 'm': 19, ' ': 63, 'i': 33, 'p': 3, 's': 31, 'u': 21, 'd': 9, 'l': 15, 't': 30, 'a': 28, ',': 3, 'c': 14, 'n': 17, 'g': 6, '.': 8, 'F': 1, 'v': 5, 'I': 1, 'f': 1, 'q': 5, 'D': 1, 'b': 1, 'h': 1, 'x': 2, 'U': 1, 'E': 1, 'P': 1, 'M': 1}
  assert len(freqs) == len(expected), "Il y a des caractères en trop ou il manque certains caractères"
  assert freqs == expected, "Dictionnaire de fréquences invalide"

def test_freqs_text4():
  assert path.exists(FILE4), f"Vous devez placer le fichier LICENCE.txt disponible sur l'UV dans {path.abspath(os.curdir)}"

  with open(FILE4) as f:
    freqs = build_freqs(f.read())
    expected = {' ': 5835, 'G': 69, 'N': 99, 'U': 60, 'E': 122, 'R': 106, 'A': 124, 'L': 141, 'P': 104, 'B': 22, 'I': 129, 'C': 78, 'S': 104, '\n': 674, 'V': 13, 'e': 3106, 'r': 2073, 's': 1581, 'i': 2037, 'o': 2503, 'n': 1804, '3': 9, ',': 313, '2': 13, '9': 4, 'J': 1, 'u': 764, '0': 14, '7': 8, 'p': 670, 'y': 597, 'g': 456, 'h': 1011, 't': 2300, '(': 45, ')': 60, 'F': 46, 'f': 663, 'w': 392, 'a': 1793, 'd': 870, 'c': 1088, '.': 218, '<': 10, ':': 11, '/': 20, '>': 10, 'v': 314, 'm': 623, 'b': 300, 'l': 800, 'T': 144, 'k': 174, '-': 24, 'W': 23, ';': 17, 'Y': 48, 'O': 94, 'x': 53, 'D': 49, '1': 28, "'": 24, 'q': 32, 'M': 33, '"': 82, 'z': 11, 'j': 27, 'H': 46, '6': 8, '4': 5, '5': 5, '8': 2, 'K': 3, 'X': 3, 'Q': 3, '`': 4}
    assert len(freqs) == len(expected), "Il y a des caractères en trop ou il manque certains caractères"
    assert freqs == expected, "Dictionnaire de fréquences invalide"



def test_tree_text1():
  plain = TEXT1
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  assert tree.char is None, "La racine ne devrait pas contenir de caractère"
  assert tree.freq == len(plain), f"La racine doit avoir une fréquence de {len(plain)}"
  assert None not in [tree.left, tree.right], "La racine devrait avoir deux nœuds enfants valides"
  assert tree.freq == tree.left.freq + tree.right.freq, "La fréquence d'un nœud est égale à la somme des fréquences de ses enfants"

def test_tree_text2():
  plain = TEXT2
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  assert tree.char is None, "La racine ne devrait pas contenir de caractère"
  assert tree.freq == len(plain), f"La racine doit avoir une fréquence de {len(plain)}"
  assert None not in [tree.left, tree.right], "La racine devrait avoir deux nœuds enfants valides"
  assert tree.freq == tree.left.freq + tree.right.freq, "La fréquence d'un nœud est égale à la somme des fréquences de ses enfants"

def test_tree_text3():
  plain = TEXT3
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  assert tree.char is None, "La racine ne devrait pas contenir de caractère"
  assert tree.freq == len(plain), f"La racine doit avoir une fréquence de {len(plain)}"
  assert None not in [tree.left, tree.right], "La racine devrait avoir deux nœuds enfants valides"
  assert tree.freq == tree.left.freq + tree.right.freq, "La fréquence d'un nœud est égale à la somme des fréquences de ses enfants"

def test_tree_text4():
  assert path.exists(FILE4), f"Vous devez placer le fichier LICENCE.txt disponible sur l'UV dans {path.abspath(os.curdir)}"

  with open(FILE4) as f:
    plain = f.read()
    freqs = build_freqs(plain)
    tree = build_huffman_tree(freqs)
    assert tree.char is None, "La racine ne devrait pas contenir de caractère"
    assert tree.freq == len(plain), f"La racine doit avoir une fréquence de {len(plain)}"
    assert None not in [tree.left, tree.right], "La racine devrait avoir deux nœuds enfants valides"
    assert tree.freq == tree.left.freq + tree.right.freq, "La fréquence d'un nœud est égale à la somme des fréquences de ses enfants"



def test_encoding_text1():
  freqs = build_freqs(TEXT1)
  tree = build_huffman_tree(freqs)
  encodings = build_encodings(tree)
  assert all(all(b in "01" for b in e) for e in encodings.values()), "L'encodage d'un caractère devrait être une chaine binaire composée de '0' et de '1'"
  assert len(set(sorted(encodings.values()))) == len(encodings.values()), "L'encodage de chaque caractère doit être différent"
  assert sorted(encodings) == ['-', 'd', 'e', 'h', 'l', 'o', 'r', 'w'], "Il y a des caractères en trop et/ou il manque certains caractères dans le dictionnaire de codage"
  assert len(encodings['l']) < len(encodings['h']), "Le caractère 'l' devrait être codé avec moins de bits que 'h'"

def test_encoding_text2():
  freqs = build_freqs(TEXT2)
  tree = build_huffman_tree(freqs)
  encodings = build_encodings(tree)
  assert all(all(b in "01" for b in e) for e in encodings.values()), "L'encodage d'un caractère devrait être une chaine binaire composée de '0' et de '1'"
  assert len(set(sorted(encodings.values()))) == len(encodings.values()), "L'encodage de chaque caractère doit être différent"
  assert sorted(encodings) == [' ', ',', 'a', 'b', 'e', 'h', 'i', 'n', 'o', 'q', 'r', 's', 't', 'u'], "Il y a des caractères en trop et/ou il manque certains caractères dans l'arbre ou dans le dictionnaire de codage"
  assert len(encodings[' ']) < len(encodings['q']), "Le caractère ' ' devrait être codé avec moins de bits que 'q'"

def test_encoding_text3():
  freqs = build_freqs(TEXT3)
  tree = build_huffman_tree(freqs)
  encodings = build_encodings(tree)
  assert all(all(b in "01" for b in e) for e in encodings.values()), "L'encodage d'un caractère devrait être une chaine binaire composée de '0' et de '1'"
  assert len(set(sorted(encodings.values()))) == len(encodings.values()), "L'encodage de chaque caractère doit être différent"
  assert sorted(encodings) == [' ', ',', '.', 'D', 'E', 'F', 'I', 'L', 'M', 'P', 'U', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x'], "Il y a des caractères en trop et/ou il manque certains caractères dans l'arbre ou dans le dictionnaire de codage"
  assert len(encodings[' ']) < len(encodings['q']), "Le caractère ' ' devrait être codé avec moins de bits que 'q'"

def test_encoding_text4():
  assert path.exists(FILE4), f"Vous devez placer le fichier LICENCE.txt disponible sur l'UV dans {path.abspath(os.curdir)}"

  with open(FILE4) as f:
    freqs = build_freqs(f.read())
    tree = build_huffman_tree(freqs)
    encodings = build_encodings(tree)
    assert all(all(b in "01" for b in e) for e in encodings.values()), "L'encodage d'un caractère devrait être une chaine binaire composée de '0' et de '1'"
    assert len(set(sorted(encodings.values()))) == len(encodings.values()), "L'encodage de chaque caractère doit être différent"
    assert sorted(encodings) == ['\n', ' ', '"', "'", '(', ')', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], "Il y a des caractères en trop ou il manque certains caractères dans l'arbre ou dans le dictionnaire de codage"
    assert len(encodings[' ']) < len(encodings['v']), "Le caractère ' ' devrait être codé avec moins de bits que 'v'"



def test_huffman_encode_len_text1():
  plain = TEXT1
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert type(compressed) == bytes, "Le type retour de huffman_encode doit être bytes"
  assert len(bytes2bin(compressed)) == 32, "La chaine compressée est incorrecte (trop ou trop peu de bits)"

def test_huffman_encode_len_text2():
  plain = TEXT2
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert type(compressed) == bytes, "Le type retour de huffman_encode doit être bytes"
  assert len(bytes2bin(compressed)) == 142, "La chaine compressée est incorrecte (trop ou trop peu de bits)"

def test_huffman_encode_len_text3():
  plain = TEXT3
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert type(compressed) == bytes, "Le type retour de huffman_encode doit être bytes"
  assert len(bytes2bin(compressed)) == 1671, "La chaine compressée est incorrecte (trop ou trop peu de bits)"

def test_huffman_encode_len_text4():
  assert path.exists(FILE4), f"Vous devez placer le fichier LICENCE.txt disponible sur l'UV dans {path.abspath(os.curdir)}"

  with open(FILE4) as f:
    plain = f.read()
    freqs = build_freqs(plain)
    tree = build_huffman_tree(freqs)
    compressed = huffman_encode(plain, tree)
    assert type(compressed) == bytes, "Le type retour de huffman_encode doit être bytes"
    assert len(bytes2bin(compressed)) == 162016, "La chaine compressée est incorrecte (trop ou trop peu de bits)"



def test_huffman_decode_text1():
  plain = TEXT1
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert huffman_decode(compressed, tree) == plain, "Erreur de décodage"

def test_huffman_decode_text2():
  plain = TEXT2
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert huffman_decode(compressed, tree) == TEXT2, "Erreur de décodage"

def test_huffman_decode_text3():
  plain = TEXT3
  freqs = build_freqs(plain)
  tree = build_huffman_tree(freqs)
  compressed = huffman_encode(plain, tree)
  assert huffman_decode(compressed, tree) == TEXT3, "Erreur de décodage"

def test_huffman_decode_text4():
  assert path.exists(FILE4), f"Vous devez placer le fichier LICENCE.txt disponible sur l'UV dans {path.abspath(os.curdir)}"

  with open(FILE4) as f:
    plain = f.read()
    freqs = build_freqs(plain)
    tree = build_huffman_tree(freqs)
    compressed = huffman_encode(plain, tree)
    assert huffman_decode(compressed, tree) == plain, "Erreur de décodage"
