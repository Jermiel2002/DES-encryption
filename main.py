#!/usr/bin/env python
# import the bitarray from the module bitarrray
from bitarray import bitarray


def encryption(data, key):
    if len(data) != 8 or len(key) != 10:
        return "La taille du message doit être de 8 bits et la clé de 10 bits."

    # Étape de permutation initiale
    data = permutation_initiale(data)

    # Diviser les données en deux moitiés de 4 bits
    middle = len(data) // 2
    left = data[:middle]
    right = data[middle:]

    # Appliquer 2 tours de substitution et permutation
    for _ in range(2):
        temp = right.copy()
        right = left ^ fonction_F(right, key)
        left = temp

    # Réassembler les moitiés
    data_chiffre = left + right

    # Appliquer une permutation inverse
    data_chiffre = permutation(data_chiffre)

    return data_chiffre


def decryption(data_chiffre, key):
    if len(data_chiffre) != 8 or len(key) != 10:
        return "La taille du message chiffré doit être de 8 bits et la clé de 10 bits."

    # Étape de permutation initiale inverse
    data_chiffre = permutation(data_chiffre, permutation_inverse)

    # Diviser les données chiffrées en deux moitiés de 4 bits
    middle = len(data_chiffre) // 2
    left = data_chiffre[:middle]
    right = data_chiffre[middle:]

    # Appliquer 2 tours de substitution et permutation en sens inverse
    for _ in range(2):
        temp = left.copy()
        left = right ^ fonction_F(left, key)
        right = temp

    # Réassembler les moitiés
    data_dechiffre = left + right

    # Appliquer une permutation initiale
    data_dechiffre = permutation(data_dechiffre, permutation_initiale)

    return data_dechiffre


# Tables de permutation initiale et inverse
permutation_initiale = [2, 6, 3, 1, 4, 8, 5, 7]
permutation_inverse = [4, 1, 3, 5, 7, 2, 8, 6]

# Table de substitution (S-box) - vous pouvez définir vos propres valeurs
s_box = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8]
]


def permutation(data, table):
    return bitarray([data[i] for i in table])


def substitution(data, s_box):
    result = bitarray()
    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]
        row = int(chunk[0] + chunk[3], 2)
        col = int(chunk[1:3], 2)
        result += bitarray(bin(s_box[row][col])[2:].zfill(4))
    return result


def fonction_F(data, key):
    # Étape de substitution
    data = substitution(data)

    # Étape de permutation
    data = permutation(data)

    # XOR avec la clé
    data ^= key

    return data


if __name__ == "__main__":
    message = bitarray(8)  # Message de 8 bits
    key = bitarray(10)  # Clé de 10 bits

    # message_chiffre = chiffrement_DES(message, key)
    # print("Données chiffrées:", message_chiffre)
