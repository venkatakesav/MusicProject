import numpy as np

# Table I: Swara-Frequency Mapping
swara_freq = {
    'Sa': 260.29, 'Ri1': 277.84, 'Ri2':293.08, 'Ga1': 293.08, 'Ri3':309.66, 'Ga2': 309.66,
    'Ga3': 330.28, 'Ma1': 346.90, 'Ma2': 372.19, 'Pa': 390.61,
    'Dha1': 414.82, 'Dha2':440.00, 'Ni1': 440.00, 'Dha3':462.33, 'Ni2': 462.33, 'Ni3': 495.84
}

# Table II: Plaintext Alphabet-Swara Sequence Mapping
alphabet_swara_Mayamalavagowla = {
    'A': 'Ma Dha', 'B': 'Ri Dha Ni', 'C': 'Sa Ma', 'D': 'Ri Ga',
    'E': 'Dha Ni', 'F': 'Sa Ri', 'G': 'Ga Ma Ni', 'H': 'Ri Dha',
    'I': 'Ga Ni', 'J': 'Ri Ga Dha', 'K': 'Ri Ma Dha', 'L': 'Sa Ni',
    'M': 'Sa Ga', 'N': 'Ga Dha', 'O': 'Ga Ma', 'P': 'Ga Ma Dha',
    'Q': 'Ri Ga Ni', 'R': 'Ri Ma', 'S': 'Ri Ni', 'T': 'Ma Ni',
    'U': 'Sa Dha', 'V': 'Ri Ma Ni', 'W': 'Ma Dha Ni', 'X': 'Ri Ga Ma',
    'Y': 'Ga Dha Ni', 'Z': 'Sa Ma Ni', ' ': 'Pa Pa'
}

def get_value(alphabet_swara, key):
    return alphabet_swara.get(key, None)

def get_key(alphabet_swara, value):
    for k, v in alphabet_swara.items():
        if v == value:
            return k
    return None

# Encryption
def encrypt(plaintext, alphabet_swara):
    ciphertext = ''
    for char in plaintext:
        if (char != ' '):
            ciphertext += alphabet_swara[char.upper()] + 'Pa'
        if char == ' ':
            ciphertext += ' Pa'
    return ciphertext

# Mapping Ri to Ri1, etc
def map_shorthand_swaras(swaras):
    full_swaras = []
    for swara in swaras:
        if swara == 'Ri':
            full_swaras.append('Ri1')
        elif swara == 'Ga':
            full_swaras.append('Ga3')
        elif swara == 'Ma':
            full_swaras.append('Ma1')
        elif swara == 'Dha':
            full_swaras.append('Dha1')
        elif swara == 'Ni':
            full_swaras.append('Ni3')
        else:
            full_swaras.append(swara)
    return full_swaras

# Music generation
def generate_freqency_list(swara_sequence):
    swara_list = []
    for word in swara_sequence.split('Pa Pa'):
        for character in word.split("Pa"):
            if(character != ""):
                swara_list.extend(character.split())
                swara_list.extend("Pa".split())
        swara_list.extend("Pa".split())
    swara_list = map_shorthand_swaras(swara_list)
    freq_list = []
    for swara in swara_list:
        freq_list.append(swara_freq[swara])
    return freq_list

# Decryption
def decrypt(ciphertext, alphabet_swara):
    plaintext = ''
    for swara_seq in ciphertext.split('Pa'):
        if swara_seq == ' ':
            plaintext += " " 
        else:
            if get_key(alphabet_swara, swara_seq):
                plaintext += get_key(alphabet_swara, swara_seq)
    return plaintext

# Example usage
plaintext = "Knowledge is power"
raga = "Mayamalavagowla"
ciphertext = encrypt(plaintext, alphabet_swara_Mayamalavagowla)
print("Ciphertext:", ciphertext)
freq_list = generate_freqency_list(ciphertext)
# music = generate_music(freq_list,alphabet_swara_Mayamalavagowla)
decrypted_text = decrypt(ciphertext, alphabet_swara_Mayamalavagowla)
print("Decrypted text:", decrypted_text)