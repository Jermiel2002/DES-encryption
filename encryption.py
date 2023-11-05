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
import time
import key_industry
# ----------------------------------------------------
#		Zone de déclaration des variables globales
# ----------------------------------------------------
# Définissez les matrices S0 et S1 en dehors de la fonction
matrice_S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
matrice_S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

# -------------------------------------------------------
#		Zone de déclaration des modules ou des fonctions
# -------------------------------------------------------



# ---------------------------------------------------------------------------------

# ----------------Sous fonctions utiles--------------------

# ---------------------------------------------------------
# deroulement du chiffremement
'''
    Fonction S-DES encryption 
    The initial Permutation is going to take 8 bit block of plaintext, and is going to make a permutation and
    going to output another 8 bit block
'''

'''Cette version utilise une compréhension de liste pour créer right_half1 en utilisant la séquence de permutation 
permutation_seq, ce qui simplifie le code et le rend plus cohérent'''
def expansion_permutation(block):
    if len(block) != 4:
        raise ValueError("La taille du 'block' doit être de 4 bits.")

    result = key_industry.permutation(block, key_industry.permutation_E_P)
    return result


'''Les S-box fonctionnenet comme suit : après l'opération XOR, les premiers et quatrième bits de chaque part sont
traités comme un nombre de 2 bits qui spécifient une ligne du sbox. Les deuxième et troisième bits spécifient la colonne
du sbox
--> Cette version améliore la lisibilité et la maintenabilité du code. En ce qui concerne sa complexité, cest exactement
la même que celle dune opération de recherche de table. On utilise utilise des S-box de 4x4, ce qui signifie qu'il y a 16 valeurs dans chaque S-box. 
Par conséquent, la complexité de l'opération S-box est constante, O(1), car elle implique simplement la recherche d'une valeur dans une petite table de substitution.'''

def s_box(part1, part2):
    result = ""
    for part in [part1, part2]:
        # Premiers 4 bits
        ligne = int(part[:1].to01()+part[3:].to01(), 2)
        colonne = int(part[1:3].to01(), 2)
        s_box_value = matrice_S0 if part is part1 else matrice_S1
        result += format(s_box_value[ligne][colonne], '02b')  # Format en binaire de longueur 2

    return bitarray(result)


def permutation_mangler(block):
    permutation_seq = [2, 4, 3, 1]
    return key_industry.permutation(block, permutation_seq)


def fonktionF(right_half, subkey):
    # right_half1 contient la première operation E/P sur le sous block droit. on obtient 8 bits
    right_half1 = expansion_permutation(right_half)
    # On fait un ou exclusive du right_half1 avec la sous clé de 8 bits
    result_xor = right_half1 ^ subkey

    # le resultat du xor passe au s-box maintenant. les 4 premiers bits sont introduits dans la boite S0
    # pour produire une sortie de 2 bits et les 4 autres restants sont introduit dans S1 pour produire une
    # autre sortie de 2 bits
    part1_of_xor = result_xor[:4]
    part2_of_xor = result_xor[4:]
    result_sbox = s_box(part1_of_xor, part2_of_xor)

    # pour le left_half, on appel la fonction switch
    return permutation_mangler(result_sbox)


'''La fonction Fk comoutput_of_ipbine la permutation et la substitution'''


def fonktionFk(output_of_ip, subkey):
    left_half, right_half = key_industry.split_bitarray(output_of_ip)
    machine_f = left_half ^ fonktionF(right_half, subkey)
    return machine_f + right_half


'''La fonction Fk n'a opérer que sur les 4 bits les plus à gauche. le switch va échanger les 4 bits à gauche
contre les 4 à droites. Ainsi la seconde instance de Fk (les 4 bits les plus à droite), sera différent. On relance ici 
fk après avoir interchangé les bits'''


def switch(data):
    left, right = key_industry.split_bitarray(data)
    return right + left



def encryption(data, key):
    # Étape de permutation initiale
    data = key_industry.permutation(data, key_industry.permutation_initiale)

    # Récupération des sous clés générées à partir de la clé initiale de 10 bits
    subkey1, subkey2 = key_industry.get_subkeys(key)
    # print("La donnée sortie de IP", data)
    a = fonktionFk(data, subkey1)
    # print("La donnée après le premier fonktionFk : ", a)
    b = switch(a)
    # print("La donnée après switch : ", b)
    c = fonktionFk(b, subkey2)
    # print("La donnée après la deuxième fonktionFk : ", c)
    message  = key_industry.permutation(c, key_industry.permutation_inverse)
    # print("La donnée après permutation inverse (permutation finale) : ", message)

    return message


def decryption(data, key):
    # Étape de permutation initiale
    data = key_industry.permutation(data, key_industry.permutation_inverse)

    # Récupération des sous clés générées à partir de la clé initiale de 10 bits
    subkey1, subkey2 = key_industry.get_subkeys(key)
    # print("La donnée sortie de IP", data)
    
    a = fonktionFk(data, subkey1)
    # print("La donnée après le premier fonktionFk : ", a)
    b = switch(a)
    # print("La donnée après switch : ", b)
    c = fonktionFk(b, subkey2)
    # print("La donnée après la deuxième fonktionFk : ", c)
    message  = key_industry.permutation(c, key_industry.permutation_initiale)
    # print("La donnée après permutation inverse (permutation finale) : ", message)

    return message


# -------------------------------------------------------
#						Appel fonctions
# -------------------------------------------------------

if __name__ == "__main__":

    print("\n\n--------------------Bienvenue dans l'univers du chiffrement SDES--------------------\n")

    bit_aleatoire = bitarray("1010000010")

    plaintext = input("Quel est votre message (8 bits): ")
    print("\nVotre message est : ", plaintext)

    message = bitarray(plaintext)

    message_chiffré = encryption(message, bit_aleatoire)

    print("\nCroyez-y et laissez la magie opérer...")
    time.sleep(5)
    print("\nBim bam boum ! voici le message chiffré : ", message_chiffré.to01())

    message_dechiffré = decryption(message_chiffré, bit_aleatoire)

    time.sleep(5)

    print("\nBim bam boum ! voici le message déchiffré : ", message_dechiffré.to01())
