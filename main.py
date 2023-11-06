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
import encryption

if __name__ == "__main__":

    print("\n\n--------------------Bienvenue dans l'univers du chiffrement SDES--------------------\n")

    bit_aleatoire = bitarray(10)

    plaintext = input("Quel est votre message (8 bits): ")
    print("\nVotre message est : ", plaintext)

    message = bitarray(plaintext)

    message_chiffré = encryption.encryption(message, bit_aleatoire)

    print("\nCroyez-y et laissez la magie opérer...")
    time.sleep(5)
    print("\nBim bam boum ! voici le message chiffré : ", message_chiffré.to01())

    message_dechiffré = encryption.decryption(message_chiffré, bit_aleatoire)

    time.sleep(5)

    print("\nBim bam boum ! voici le message déchiffré : ", message_dechiffré.to01())
