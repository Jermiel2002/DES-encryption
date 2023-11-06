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

# Tables de permutation initiale et inverse
permutation_initiale = [2, 6, 3, 1, 4, 8, 5, 7] #IP
permutation_inverse = [4, 1, 3, 5, 7, 2, 8, 6] #IP^-1

# Tables de permutation P10 et P8
permutation_p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6] #P10
permutation_p8 = [6, 3, 7, 4, 8, 5, 10, 9] #P8

#Tables de permutation 
permutation_E_P = [4, 1, 2, 3, 2, 3, 4, 1]#Expansion/Permutation

# -------------------------------------------------------
#		Zone de déclaration des modules ou des fonctions
# -------------------------------------------------------
'''split_bitarray permet de diviser la clé de n bit en un tuple contenant deux bitarray
avec les 5 premiers et les 5 derniers bits
--> J'ai également modifié la fonction pour qu'elle renvoie directement des instances de bitarray 
en convertissant les tranches bitarray1 et bitarray2. Cela améliore la lisibilité du code et garantit que les sorties sont bien des bitarray.'''
def split_bitarray(data):
    n = len(data)

    if n % 2 != 0:
        raise ValueError("La taille du bitarray doit être un multiple de 2.")

    middle = n // 2
    left = data[:middle]
    right = data[middle:]

    return bitarray(left), bitarray(right)


'''Après permutation on effectue un décalage gauche de 1 séparement : sur les premiers 5 bits
et sur les derniers 5 bits
---> implémentation actuelle est correcte, mais elle peut être améliorée en utilisant la méthode 
rotate des bitarrays de la bibliothèque bitarray pour simplifier le code.'''


def l_circular_shift(key_tuple, n=1):
    '''Explication du principe du left circular shift
    Pour effectuer un décalage circulaire vers la gauche d'un nombre binaire 10000 de manière à obtenir 00001,
    on doit décaler de 1 position vers la gauche. Voici comment cela fonctionne :
        1- on a la sequence binaire 10000
        2- on effectue le décalage circulaire de 1 position
        3- le bit decalé est 1
        4- On reinsère ce bit à droit de la sequence
        --> elle est optimisée en termes de lisibilité, de simplicité et de conformité avec la bibliothèque bitarray
    '''
    try:
        key_tuple = split_bitarray(key_tuple)
        part1, part2 = key_tuple
    except:
        part1, part2 = key_tuple

    # Effectuer le décalage circulaire vers la gauche de deux positions
    result_part1 = part1[n:] + part1[:n]
    result_part2 = part2[n:] + part2[:n]
    result = result_part1 + result_part2

    return result


def permutation(data, table):
    return bitarray(data[i - 1] for i in table)


def get_subkeys(key):
    # Effectue une permutation initiale
    bit_permute = permutation(key, permutation_p10) #Permutation P10

    # Effectue un décalage circulaire (rotation)
    first_last5_bit = split_bitarray(bit_permute)
    rotation1 = l_circular_shift(first_last5_bit)

    # Effectue une autre permutation pour obtenir la première sous-clé
    subkey1 = permutation(rotation1, permutation_p8) #Permutation P8

    # Effectue un deuxième décalage circulaire pour obtenir la deuxième sous-clé
    rotation2 = l_circular_shift(rotation1, 2)
    subkey2 = permutation(rotation2, permutation_p8) #Permutation P8

    return (subkey1, subkey2)


# --------------------------------------------------------------------------------------
def generate_key():
    # Génère une clé aléatoire de 10 bits
    bit_aleatoire = bitarray("1010000010")
    print("La clé de 10 bits aléatoires générées est : ", bit_aleatoire)

    return get_subkeys(bit_aleatoire)