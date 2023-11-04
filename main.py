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
import encryption

if __name__ == "__main__":
    print("\n\n--------------------Bienvenue dans l'univers du chiffrement SDES--------------------\n")
    clé = key_industry.generate_key()
    print("\n$Pour commencer on va utiliser la clé suivante pour le chiffrement et le déchiffrement$ : ",clé)
    subkey1 = clé[0]
    subkey2 = clé[1]
    print("\n_______________A partir de cette clé, on va générée deux sous clé_______________\n")
    print("\nla première sous-clés obtenue est : \n", subkey1)
    print("\nla deuxième sous-clés obtenue est : \n", subkey2)

    action = None

    while action not in [1, 2]:
        try:
            action = int(input("Que voulez vous faire ?\n Entrer 1 pour le chiffrement\n Entrer 2 pour le déchiffrement \nAlors ? : "))
            if action not in [1, 2]:
                print("Choix invalide. Veuillez entrer 1 ou 2.")
        except ValueError:
            print("Choix invalide. Veuillez entrer 1 ou 2 (en tant que nombre entier).")

    if (action == 1):
        print("\n**************Bienvenue ! Je vais vous aider à chiffrer votre message**************\n")
        plaintext = input("Quel est votre message (8 bits): ")
        plaintext_useable = bitarray(plaintext)
        print("\nVotre message est : ", plaintext_useable)
        a = encryption.fonktionFk(plaintext_useable, subkey1)
        # print("les 4 bits les plus à gauche : ", a)
        b = encryption.switch(a)
        # print("le switch donne : ", b)
        c = bitarray(b[0] + b[1])
        # print("prêt à envoyer : ", c)
        d = encryption.fonktionFk(c, subkey2)
        # print("la deuxième application donne : ", d)
        # on converti le resultat en un seul bit array
        e = bitarray(d[0] + d[1])
        # on fait une permutation finale sur d
        message = encryption.final_permutationIP(e)
        print("Croyez-y et laissez la magie opèrer...")
        time.sleep(2)
        print("Bim bam boum ! voici le message chiffrer : ", message)
    elif (action == 2):
        print("\n**************Bienvenue ! Je vais vous aider à déchiffrer votre message**************\n")
        plaintext = input("Quel est le message chiffré (8 bits): ")
        plaintext_useable = bitarray(plaintext)
        print("Le code de déchiffrement n'est malheureusement pas encore prêt ! veuillez réessayer plus tard ! Merci")
