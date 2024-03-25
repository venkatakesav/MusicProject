import numpy as np
from pydub import AudioSegment
# from pydub.generators import sine_wave

# Table I: Swara-Frequency Mapping
swara_freq = {
    'Sa': 260.29, 'Ri1': 277.84, 'Ri2, Ga1': 293.08, 'Ri3, Ga2': 309.66,
    'Ga3': 330.28, 'Ma1': 346.90, 'Ma2': 372.19, 'Pa': 390.61,
    'Dha1': 414.82, 'Dha2, Ni1': 440.00, 'Dha3, Ni2': 462.33, 'Ni3': 495.84
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

# Music generation
# def generate_music(swara_sequence, sample_rate=44100):
#     music = AudioSegment.silent(duration=0)
#     for rage in swara_sequence.split('Pa'):
#         if swara == '':
#             continue
#         freq = [swara_freq[s] for s in swara.split()]
#         duration = 0.5  # Duration of each note in seconds
#         samples = np.linspace(0, duration, int(duration * sample_rate), False)
#         wave = np.sum([sine_wave(samples, freq=f, volume=-6.0) for f in freq], axis=0)
#         music += AudioSegment(wave.astype(np.int16), frame_rate=sample_rate, channels=1)
#     # return music

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
# music = generate_music(ciphertext)
# music.export("output.wav", format="wav")
decrypted_text = decrypt(ciphertext, alphabet_swara_Mayamalavagowla)
print("Decrypted text:", decrypted_text)