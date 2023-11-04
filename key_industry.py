"""
Nom du TP : Sécurité et théorie de l'information

Auteurs : Jermiel Kpessou KOUNOUHO & Mohammed Ibrahim DJIBRILA

Numéros étudiants : 12001045 & 12313574

source : https://www.youtube.com/watch?v=nynAQ593HdU&list=PLBlnK6fEyqRiOCCDSdi6Ok_8PU2f_nkuf&index=3
"""
# -----------------------------------------------------------------------------
#
#
# -----------------------------------------------------------------------------


################################################
#				Programme principal
################################################

# -----------------------------------------------
#		    Zone des 'imports' de modules
# -----------------------------------------------
from bitarray import bitarray
import random
import time

# ----------------------------------------------------
#		Zone de déclaration des variables globales
# ----------------------------------------------------
subkey1 = bitarray()
subkey2 = bitarray()


# -------------------------------------------------------
#		Zone de déclaration des modules ou des fonctions
# -------------------------------------------------------
'''split_bitarray permet de diviser la clé de n bit en un tuple contenant deux bitarray
avec les 5 premiers et les 5 derniers bits
--> J'ai également modifié la fonction pour qu'elle renvoie directement des instances de bitarray 
en convertissant les tranches bitarray1 et bitarray2. Cela améliore la lisibilité du code et garantit que les sorties sont bien des bitarray.'''
def split_bitarray(key):
    n = len(key)

    if n % 2 != 0:
        raise ValueError("La taille du bitarray doit être un multiple de 2.")

    milieu = n // 2
    bitarray1 = key[:milieu]
    bitarray2 = key[milieu:]

    return bitarray(bitarray1), bitarray(bitarray2)

'''Première permutation de la clé de 10 bits généré. Chaque chiffre dans le tableau donne la position du bit à récupérer
et l'indice de ce chiffre dans le tableau indique la position du bit après permutation

--> on peut utiliser une approche plus concise en utilisant une compréhension de liste et en évitant la boucle for'''

def permute_key(key):
    permutation_seq = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    bit_permutter = bitarray(key[i] for i in permutation_seq)
    return bit_permutter


'''Après permutation on effectue un décalage gauche de 1 séparement : sur les premiers 5 bits
et sur les derniers 5 bits
---> implémentation actuelle est correcte, mais elle peut être améliorée en utilisant la méthode 
rotate des bitarrays de la bibliothèque bitarray pour simplifier le code.'''


def l_circular_shift(key_tuple):
    '''Explication du principe du left circular shift
    Pour effectuer un décalage circulaire vers la gauche d'un nombre binaire 10000 de manière à obtenir 00001,
    on doit décaler de 1 position vers la gauche. Voici comment cela fonctionne :
        1- on a la sequence binaire 10000
        2- on effectue le décalage circulaire de 1 position
        3- le bit decalé est 1
        4- On reinsère ce bit à droit de la sequence
        --> elle est optimisée en termes de lisibilité, de simplicité et de conformité avec la bibliothèque bitarray
    '''
    part1, part2 = key_tuple

    # Effectuer le décalage circulaire vers la gauche d'une position
    bit1 = part1.pop(0)  # Supprimez le premier bit de part1
    bit2 = part2.pop(0)  # Supprimez le premier bit de part2

    part1.append(bit1)  # Ajoutez le bit supprimé à la fin de part1
    part2.append(bit2)  # Ajoutez le bit supprimé à la fin de part2

    result = part1 + part2
    # result_part1 = part1 << 1 #ici normalement on doit utilisé le symbole de decalage mais quand je l'utilise
    # j'obtiens vite un set de 0. On a l'impression python fais mal le décalage
    # result_part2 = part2 << 1
    return result


'''On refait ensuite une nouvelle permutation appelé P8 qui sélectionne et permute 8 bits
sur les 10 renvoyé précedemment. Le résultat renvoyé est la clé 1
--> nous utilisons une compréhension de liste pour créer bit_permutter en utilisant la séquence de permutation permutation_seq. 
Cela simplifie le code tout en maintenant la même fonctionnalité que la version précédente'''


def permute_keyP8(key):
    permutation_seq = [5, 2, 6, 3, 7, 4, 9, 8]
    bit_permutter = bitarray(key[i] for i in permutation_seq)
    return bit_permutter


def l_circular_shift2(key):
    '''Explication du principe du left circular shift
    Pour effectuer un décalage circulaire vers la gauche d'un nombre binaire 10000 de manière à obtenir 00001,
    on doit décaler de 2 position vers la gauche. Voici comment cela fonctionne :
        1- on a la sequence binaire 10000
        2- on effectue le décalage circulaire de 2 position
        3- le bit decalé est 10
        4- On reinsère ce bit à droit de la sequence et on a 00010
    '''
    key_tuple = split_bitarray(key)
    part1, part2 = key_tuple
    # Effectuer le décalage circulaire vers la gauche de deux positions
    result_part1 = part1[2:] + part1[:2]
    result_part2 = part2[2:] + part2[:2]
    result = result_part1 + result_part2
    return result

# --------------------------------------------------------------------------------------
def generate_key():
    # Génère une clé aléatoire de 10 bits
    bit_aleatoire = bitarray(''.join(str(random.randint(0, 1)) for _ in range(10)))
    print("La clé de 10 bits aléatoires générées est : ", bit_aleatoire)

    # Effectue une permutation initiale
    bit_permute = permute_key(bit_aleatoire)

    # Effectue un décalage circulaire (rotation)
    first_last5_bit = split_bitarray(bit_permute)
    rotation1 = l_circular_shift(first_last5_bit)

    # Effectue une autre permutation pour obtenir la première sous-clé
    key1 = permute_keyP8(rotation1)

    # Effectue un deuxième décalage circulaire pour obtenir la deuxième sous-clé
    rotation2 = l_circular_shift2(rotation1)
    key2 = permute_keyP8(rotation2)

    return (key1, key2)