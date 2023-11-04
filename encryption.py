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
    permutation_seq = [1, 5, 2, 0, 3, 7, 4, 6]
    block1 = bitarray(plaintext[i] for i in permutation_seq)
    return block1

'''Cette version utilise une compréhension de liste pour créer right_half1 en utilisant la séquence de permutation 
permutation_seq, ce qui simplifie le code et le rend plus cohérent'''
def expansion_permutation(block):
    permutation_seq = (3, 0, 1, 2, 1, 2, 3, 0)

    if len(block) != 4:
        raise ValueError("La taille de 'block' doit être de 4 bits.")

    right_half1 = bitarray(block[i] for i in permutation_seq)

    return right_half1

'''Bien que notre ancienne version soit correcte, cette version utilise une liste selected_bits pour stocker 
les bits sélectionnés, puis les convertit en une bitarray. Juste deux lignes de codes'''
def select_bits(part_of_4_bit, pos1, pos2):
    # Sélectionnez les bits aux positions désirées
    selected_bits = [part_of_4_bit[pos1], part_of_4_bit[pos2]]

    # Créez une nouvelle bitarray en utilisant les bits sélectionnés
    new_bitarray = bitarray(selected_bits)

    return new_bitarray


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
        ligne = int(part[:1].to01(), 2)
        colonne = int(part[1:3].to01(), 2)
        s_box_value = matrice_S0 if part is part1 else matrice_S1
        result += format(s_box_value[ligne][colonne], '02b')  # Format en binaire de longueur 2

    return result

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
    permutation_seq = [3, 0, 2, 4, 6, 1, 7, 5]
    block_end = bitarray(plaintext[i] for i in permutation_seq)
    return block_end


# -------------------------------------------------------
#						Appel fonctions
# -------------------------------------------------------

if __name__ == "__main__":

    #print("\n\n--------------------Bienvenue dans l'univers du chiffrement SDES--------------------\n")
    clé = key_industry.generate_key()
    subkey1 = clé[0]
    subkey2 = clé[1]
    print("\nla première sous-clés obtenue est : \n", subkey1)
    print("\nla deuxième sous-clés obtenue est : \n", subkey2)

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
