import numpy as np
from typing import Dict, Tuple

# Define the mapping tables
MAPPING_TABLES = {
    "Mayamalavagowla": {
        "alphabet_to_swara": {
            "A": "Ma Dha", "B": "Ri Dha Ni", "C": "Sa Ma", "D": "Ri Ga",
            "E": "Dha Ni", "F": "Sa Ri", "G": "Ga Ma Ni", "H": "Ri Dha",
            "I": "Ga Ni", "J": "Ri Ga Dha", "K": "Ri Ma Dha", "L": "Sa Ni",
            "M": "Sa Ga", "N": "Ga Dha", "O": "Ga Ma", "P": "Ga Ma Dha",
            "Q": "Ri Ga Ni", "R": "Ri Ma", "S": "Ri Ni", "T": "Ma Ni",
            "U": "Sa Dha", "V": "Ri Ma Ni", "W": "Ma Dha Ni", "X": "Ri Ga Ma",
            "Y": "Ga Dha Ni", "Z": "Sa Ma Ni", " ": "Pa Pa"
        },
        "amsa_swara": "Pa"
    },
    "Harikambhoji": {
        "alphabet_to_swara": {
            "A": "Ri Ma", "B": "Ga Dha Ni", "C": "Sa Ga", "D": "Ri Dha",
            "E": "Ga Ni", "F": "Sa Ri", "G": "Dha Ni Sa", "H": "Ri Ga",
            "I": "Ga Ma", "J": "Ri Dha Ni", "K": "Ri Ga Dha", "L": "Sa Dha",
            "M": "Ga Ma", "N": "Dha Ni", "O": "Ga Ri", "P": "Ga Ma Dha",
            "Q": "Ri Ni Sa", "R": "Ri Ga", "S": "Ri Dha", "T": "Ma Dha",
            "U": "Sa Ni", "V": "Ri Ma", "W": "Dha Ni Sa", "X": "Ri Ga Ma",
            "Y": "Ga Dha Ni", "Z": "Sa Ri", " ": "Ma Ma"
        },
        "amsa_swara": "Ma"
    }
}

def encrypt(plaintext: str, raga: str) -> str:
    mapping = MAPPING_TABLES[raga]["alphabet_to_swara"]
    amsa_swara = MAPPING_TABLES[raga]["amsa_swara"]
    ciphertext = ""
    for char in plaintext:
        ciphertext += mapping[char.upper()] + "Pa"
        if char == " ":
            ciphertext += amsa_swara * 2
        else:
            ciphertext += amsa_swara
    return ciphertext

def decrypt(ciphertext: str, raga: str) -> str:
    mapping = {v: k for k, v in MAPPING_TABLES[raga]["alphabet_to_swara"].items()}
    amsa_swara = MAPPING_TABLES[raga]["amsa_swara"]
    plaintext = ""
    swara_sequence = ""
    for swara in ciphertext.split("Pa"):
        if swara == amsa_swara * 2:
            plaintext += " "
        else:
            plaintext += mapping[swara]
    return plaintext

# Example usage
plaintext = "Knowledge is power"
ciphertext = encrypt(plaintext, "Mayamalavagowla")
print(f"Plaintext: {plaintext}")
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted text: {decrypt(ciphertext, 'Mayamalavagowla')}")