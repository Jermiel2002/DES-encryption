"""
Nom du TP : Sécurité et théorie de l'information

Auteur : Jermiel Kpessou KOUNOUHO

Numéro étudiant : 12001045

Révision N° : Version 1

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
#----------------------------------------------------
#		Zone de déclaration des variables globales
#----------------------------------------------------


#-------------------------------------------------------
#		Zone de déclaration des modules ou des fonctions
#-------------------------------------------------------
'''Fonction de génération de clé de 10 bits'''

def permute_key(key):
    taille = len(key)
    bit_permutter = bitarray()
    permutation_seq = [2,4,1,6,3,9,0,8,7,5]
    for i in range(taille):
        val_insert = key[permutation_seq[i]]
        bit_permutter.append(val_insert)
    return bit_permutter

def l_circular_shift(key_tuple):
    '''Explication du principe du left circular shift
    Pour effectuer un décalage circulaire vers la gauche d'un nombre binaire 10000 de manière à obtenir 00001,
    on doit décaler de 1 position vers la gauche. Voici comment cela fonctionne :
        1- on a la sequence binaire 10000
        2- on effectue le décalage circulaire de 1 position
        3- le bit decalé est 1
        4- On reinsère ce bit à droit de la sequence
    '''
    part1 = key_tuple[0]
    part2 = key_tuple[1]
    result_part1 = part1[1:] + part1[:1] #key[1:] = extrait a partir du bit à l'index 1 jusqu'à la fin
    result_part2 = part2[1:] + part2[:1]
    result = result_part1 + result_part2
    return result
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
    part1 = key_tuple[0]
    part2 = key_tuple[1]
    result_part1 = part1[2:] + part1[:2] #key[2:] = extrait a partir du bit à l'index 2 jusqu'à la fin
    result_part2 = part2[2:] + part2[:2]
    result = result_part1 + result_part2
    return result
def permute_keyP8(key):
    bit_initial = key
    bit_permutter = bitarray()
    permutation_seq = [5,2,6,3,7,4,9,8]
    taille = len(permutation_seq)
    for i in range (taille):
        val_insert = bit_initial[permutation_seq[i]]
        bit_permutter.append(val_insert)
    return bit_permutter
'''split_bitarray permet de diviser la clé de 10 bit en un tuple contenant deux bitarray
avec les 5 premiers et les 5 derniers bits'''
def split_bitarray(key):
    n = len(key)
    if n % 2 != 0:
        raise ValueError("La taille du bitarray doit être un multiple de 2.")
    milieu = n // 2
    bitarray1 = key[:milieu]
    bitarray2 = key[milieu:]
    return (bitarray1,bitarray2)

def generate_key():
    bit_aleatoire = bitarray(10)
    #print(bit_aleatoire)
    '''On va permutter le bit aleatoire créer; bit_permute contient l'array de la clé permuter'''
    bit_permute = permute_key(bit_aleatoire)

    '''On va effectuer un décalage circulaire vers la gauche (circular left shift LS-1),
       encore appelé rotation.
       Cette opération sera faite séparement : sur les 5 premiers bits et sur les 5 autres'''
    first_last5_bit = split_bitarray(bit_permute) #renvoie un tuple de bitarray, l'un contient les premières cinq element et l'autre les 5 dernières
    rotation1 = l_circular_shift(first_last5_bit) #on effectue l'opération de decalage sur chaque tuple et return les 10 bits

    '''On effectue une autre permutation et on a la première sous clé'''
    key1 = permute_keyP8(rotation1)

    '''Creation de la deuxième sous clé: on effectue cette fois un décalage de 2 position vers la gauche
    sur le resultat obtenu du dernier décalage'''
    rotation2 = l_circular_shift2(rotation1)
    key2 = permute_keyP8(rotation2)
    return (key1,key2)
#-------------------------------------------------------
#						Appel fonctions
#-------------------------------------------------------
cle = generate_key()
print("voici les deux sous clé : ", cle)

''' exemple avec le bitarray dans le pdf explication du s-des
a = split_bitarray(bitarray('1000001100'))
print(a)
b = l_circular_shift(a)
print(b)
c = permute_keyP8(b)
print(c)
d = l_circular_shift2(b)
print(d)'''