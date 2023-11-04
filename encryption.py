"""
Nom du TP : Sécurité et théorie de l'information

Auteurs : Jermiel Kpessou KOUNOUHO &

Numéros étudiants : 12001045 &

Révision N° : Version 1

source : https://www.youtube.com/watch?v=nynAQ593HdU&list=PLBlnK6fEyqRiOCCDSdi6Ok_8PU2f_nkuf&index=3
"""
import random
import time

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

# ----------------------------------------------------
#		Zone de déclaration des variables globales
# ----------------------------------------------------
subkey1 = bitarray()
subkey2 = bitarray()

# -------------------------------------------------------
#		Zone de déclaration des modules ou des fonctions
# -------------------------------------------------------
'''Fonction de génération de clé de 10 bits---------------------------------------------------'''

'''Première permutation de la clé de 10 bits généré. Chaque chiffre dans le tableau donne la position du bit à récupérer
et l'indice de ce chiffre dans le tableau indique la position du bit après permutation'''


def permute_key(key):
    taille = len(key)
    bit_permutter = bitarray()
    permutation_seq = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    for i in range(taille):
        val_insert = key[permutation_seq[i]]
        bit_permutter.append(val_insert)
    return bit_permutter


'''Après permutation on effectue un décalage gauche de 1 séparement : sur les premiers 5 bits
et sur les derniers 5 bits'''


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
    result_part1 = part1[1:] + part1[:1]  # key[1:] = extrait a partir du bit à l'index 1 jusqu'à la fin
    result_part2 = part2[1:] + part2[:1]
    # result_part1 = part1 << 1 #ici normalement on doit utilisé le symbole de decalage mais quand je l'utilise
    # j'obtiens vite un set de 0. On a l'impression python fais mal le décalage
    # result_part2 = part2 << 1
    result = result_part1 + result_part2
    return result


'''On refait ensuite une nouvelle permutation appelé P8 qui sélectionne et permute 8 bits
sur les 10 renvoyé précedemment. Le résultat renvoyé est la clé 1'''


def permute_keyP8(key):
    bit_initial = key
    bit_permutter = bitarray()
    permutation_seq = [5, 2, 6, 3, 7, 4, 9, 8]
    taille = len(permutation_seq)
    for i in range(taille):
        val_insert = bit_initial[permutation_seq[i]]
        bit_permutter.append(val_insert)
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
    part1 = key_tuple[0]
    part2 = key_tuple[1]
    result_part1 = part1[2:] + part1[:2]  # key[2:] = extrait a partir du bit à l'index 2 jusqu'à la fin
    result_part2 = part2[2:] + part2[:2]
    # result_part1 = part1 << 2
    # result_part2 = part2 << 2
    result = result_part1 + result_part2
    return result


'''split_bitarray permet de diviser la clé de n bit en un tuple contenant deux bitarray
avec les 5 premiers et les 5 derniers bits'''


def split_bitarray(key):
    n = len(key)
    if n % 2 != 0:
        raise ValueError("La taille du bitarray doit être un multiple de 2.")
    milieu = n // 2
    bitarray1 = key[:milieu]
    bitarray2 = key[milieu:]
    return (bitarray1, bitarray2)


# --------------------------------------------------------------------------------------
def generate_key():
    # creer un bitarray vide
    bit_aleatoire = bitarray()

    # remplir le bitarray avec des valeurs aléatoires (0 ou 1)
    for _ in range(10):
        bit_aleatoire.append(random.choice([0, 1]))
    print("La clé de 10 bits aléatoires générées est : ", bit_aleatoire)

    '''On va permutter le bit aleatoire créer; bit_permute contient l'array de la clé permuter'''
    bit_permute = permute_key(bit_aleatoire)

    '''On va effectuer un décalage circulaire vers la gauche (circular left shift LS-1),
       encore appelé rotation.
       Cette opération sera faite séparement : sur les 5 premiers bits et sur les 5 autres'''
    first_last5_bit = split_bitarray(
        bit_permute)  # renvoie un tuple de bitarray, l'un contient les premières cinq element et l'autre les 5 dernières
    rotation1 = l_circular_shift(
        first_last5_bit)  # on effectue l'opération de decalage sur chaque élément de notre tuple et return les 10 bits

    '''On effectue une autre permutation et on a la première sous clé'''
    key1 = permute_keyP8(rotation1)

    '''Creation de la deuxième sous clé: on effectue cette fois un décalage de 2 position vers la gauche
    sur le resultat obtenu du dernier décalage'''
    rotation2 = l_circular_shift2(rotation1)
    key2 = permute_keyP8(rotation2)

    return (key1, key2)


# ---------------------------------------------------------------------------------

# ----------------Sous fonctions utiles--------------------

# ---------------------------------------------------------
# deroulement du chiffremement
'''
    Fonction S-DES encryption 
    The initial Permutation is going to take 8 bit block of plaintext, and is going to make a permutation and
    going to output another 8 bit block
'''
'''Permutation initiale'''


def initial_permutation_ip(plaintext):
    taille = len(plaintext)
    block1 = bitarray()
    permutation_seq = [1, 5, 2, 0, 3, 7, 4, 6]
    for i in range(taille):
        val_insert = plaintext[permutation_seq[i]]
        block1.append(val_insert)
    return block1


def expansion_permutation(block):
    permutation_seq = (3, 0, 1, 2, 1, 2, 3, 0)

    if len(block) != 4:
        raise ValueError("La taille de 'block' doit être de 4 bits.")

    right_half1 = bitarray()

    for i in permutation_seq:
        val_insert = block[i]
        right_half1.append(val_insert)

    return right_half1


'''def expansion_permutation(block):
    block_useable = list(block)
    print(type(block_useable))
    #block_useable = bitarray(block)
    permutation_seq = (3, 0, 1, 2, 1, 2, 3, 0)
    right_half1 = bitarray()

    for i in permutation_seq:
        #print(type(block[i]))
        val_insert = block_useable[i]
        right_half1.append(val_insert)

    return right_half1'''


def select_bits(part_of_4_bit, pos1, pos2):
    # on selectione les positions desirée
    bit_1 = part_of_4_bit[pos1]
    bit_2 = part_of_4_bit[pos2]

    # on crée une nouvelle bitarray en fusionnant les bits selectionnées
    new_bitarray = bitarray()
    new_bitarray.extend([bit_1, bit_2])

    return new_bitarray


'''Les S-box fonctionnenet comme suit : après l'opération XOR, les premiers et quatrième bits de chaque part sont
traités comme un nombre de 2 bits qui spécifient une ligne du sbox. Les deuxième et troisième bits spécifient la colonne
du sbox'''


def s_box(part1, part2):
    matrice_S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    matrice_S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    # premiers 4 bits
    POP3_elmt1 = select_bits(part1, 0, 3)
    P1P2_elmt1 = select_bits(part1, 1, 2)
    # on converti en entier les resultats
    ligne1 = int(POP3_elmt1.to01(), 2)
    colonne1 = int(P1P2_elmt1.to01(), 2)
    # On renvoie la valeur de l'élement correspondant à la ligne et à la colonne dans le sbox
    first_elmt = matrice_S0[ligne1][colonne1]

    # deuxième 4 bits
    POP3_elmt2 = select_bits(part2, 0, 3)
    P1P2_elmt2 = select_bits(part2, 1, 2)
    # on converti en entier les resultats
    ligne2 = int(POP3_elmt2.to01(), 2)
    colonne2 = int(P1P2_elmt2.to01(), 2)
    # On renvoie la valeur de l'élement correspondant à la ligne et à la colonne dans le sbox
    snd_elmt = matrice_S1[ligne2][colonne2]

    '''#on converti first_elmt et snd_elmt en binaire et après on les fusionnes
    convert_first = bin(first_elmt)[2:] #[2:] pour enlever le préfixe 'Ob' du resultat
    bin_first = bitarray(convert_first)
    convert_snd = bin(snd_elmt)[2:]
    bin_snd = bitarray(convert_snd)
    fusion = bitarray()
    fusion.extend([bin_first,bin_snd])
    return fusion'''
    fusion = first_elmt + snd_elmt
    # on converti le resultat de la fusion en binaire de longueur 4
    fusion_bin = bin(fusion)[2:]
    fusion_bin = fusion_bin.zfill(4)
    return fusion_bin


def permutation_mangler(block):
    taille = len(block)
    block_useable = bitarray(block)
    # print(type(block))
    bit_permutter = bitarray()
    permutation_seq = [1, 3, 2, 0]
    for i in range(taille):
        val_insert = block_useable[permutation_seq[i]]
        bit_permutter.append(val_insert)
    return bit_permutter


def fonktionF(right_half, key):
    # print("beljdj",right_half)
    # right_half1 contient la première operation E/P sur le sous block droit. on obtient 8 bits
    right_half1 = expansion_permutation(right_half)

    # On fait un ou exclusive du right_half1 avec la sous clé 1 de 8 bits
    result_xor = right_half1 ^ key

    # le resultat du xor passe au s-box maintenant. les 4 premiers bits sont introduits dans la boite S0
    # pour produire une sortie de 2 bits et les 4 autres restants sont introduit dans S1 pour produire une
    # autre sortie de 2 bits
    part1_of_xor = result_xor[:4]
    part2_of_xor = result_xor[4:]
    result_sbox = s_box(part1_of_xor, part2_of_xor)
    res_final = permutation_mangler(result_sbox)

    # pour le left_half, on appel la fonction switch
    return res_final


'''La fonction Fk combine la permutation et la substitution'''


def fonktionFk(output_of_ip, key):
    split_ip = split_bitarray(output_of_ip)
    left_half = split_ip[0]
    right_half = split_ip[1]
    #print("le right bizarre : ", right_half)
    #print("pourtant le split_ip donne : ", split_ip)
    machine_f = left_half ^ fonktionF(right_half, key)
    return (machine_f, right_half)


'''La fonction Fk n'a opérer que sur les 4 bits les plus à gauche. le switch va échanger les 4 bits à gauche
contre les 4 à droites. Ainsi la seconde instance de Fk (les 4 bits les plus à droite), sera différent. On relance ici 
fk après avoir interchangé les bits'''


def switch(output_of_fonktionFk):
    echange_4_bits_L_R = (output_of_fonktionFk[1], output_of_fonktionFk[0])
    return echange_4_bits_L_R


'''Permutation final'''


def final_permutationIP(plaintext):
    taille = len(plaintext)
    block_end = bitarray()
    permutation_seq = [3, 0, 2, 4, 6, 1, 7, 5]
    for i in range(taille):
        val_insert = plaintext[permutation_seq[i]]
        block_end.append(val_insert)
    return block_end


# -------------------------------------------------------
#						Appel fonctions
# -------------------------------------------------------

if __name__ == "__main__":
    print("\n\n--------------------Bienvenue dans l'univers du chiffrement SDES--------------------\n")
    clé = generate_key()
    subkey1 = clé[0]
    subkey2 = clé[1]
    #print("\nla première sous-clés obtenue est : \n", subkey1)
    #print("\nla deuxième sous-clés obtenue est : \n", subkey2)

    plaintext = input("Quel est votre message (8 bits): ")
    plaintext_useable = bitarray(plaintext)
    print("\nVotre message est : ", plaintext_useable)
    a = fonktionFk(plaintext_useable, subkey1)
    #print("les 4 bits les plus à gauche : ", a)
    b = switch(a)
    #print("le switch donne : ", b)
    c = bitarray(b[0]+b[1])
    #print("prêt à envoyer : ", c)
    d = fonktionFk(c, subkey2)
    #print("la deuxième application donne : ", d)
    #on converti le resultat en un seul bit array
    e = bitarray(d[0]+d[1])
    #on fait une permutation finale sur d
    message  = final_permutationIP(e)
    print("Croyez-y et laissez la magie opèrer...")
    time.sleep(2)
    print("Bim bam boum ! voici le message chiffrer : ", message)
