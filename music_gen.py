import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile

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
def decrypt_ciphertext(ciphertext, alphabet_swara):
    plaintext = ''
    for swara_seq in ciphertext.split('Pa'):
        if swara_seq == ' ':
            plaintext += " " 
        else:
            if get_key(alphabet_swara, swara_seq):
                plaintext += get_key(alphabet_swara, swara_seq)
    return plaintext

def generate_audio_sequence(frequency_list, duration=0.5, sampling_rate=44100, output_file="audio_sequence.wav"):
    """
    Generate an audio sequence based on a list of frequencies and write it to a WAV file.

    Parameters:
        frequency_list (list): List of frequencies for each tone.
        duration (float): Duration of each tone in seconds. Defaults to 0.5 seconds.
        sampling_rate (int): Sampling rate in Hz. Defaults to 44100 Hz.
        output_file (str): Output file path for the generated WAV file. Defaults to "audio_sequence.wav".

    Returns:
        None
    """
    # Function to generate sine wave for a given frequency
    def generate_sine_wave(frequency, duration, sampling_rate):
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        return np.sin(2 * np.pi * frequency * t)

    # Generate audio sequence
    audio_sequence = np.array([])
    for freq in frequency_list:
        audio_sequence = np.concatenate((audio_sequence, generate_sine_wave(freq, duration, sampling_rate)))

    # Scale audio sequence to 16-bit integers
    audio_sequence *= 32767 / np.max(np.abs(audio_sequence))
    audio_sequence = audio_sequence.astype(np.int16)

    # Write audio sequence to a WAV file
    write(output_file, sampling_rate, audio_sequence)

# Function to get frequency list from audio file
def get_frequency_list(audio_file, window_size, overlap,swara_freq):

    sampling_rate, data = wavfile.read(audio_file)
    
    frequency_list = []
    
    step_size = int(window_size * (1 - overlap))
    
    # Iterate through audio data with the given step size
    for i in range(0, len(data), step_size):

        window = data[i:i+window_size]        
        fft_result = np.fft.fft(window)        
        frequencies = np.fft.fftfreq(len(window), 1 / sampling_rate)        
        max_index = np.argmax(np.abs(fft_result))
        max_frequency = np.abs(frequencies[max_index])
        frequency_list.append(max_frequency)
    
    nearest_swara = []
    for freq in frequency_list:
        nearest = min(swara_freq.values(), key=lambda x: abs(x - freq))
        nearest_swara.append([key for key, value in swara_freq.items() if value == nearest][0])
    return nearest_swara

# def decrypt_swara(swara_list, alphabet_swara):
#     plaintext = ''
#     words=[]
#     word_list = []
#     for i in range(len(swara_list)-1):
#         if(swara_list[i]=="Pa" and swara_list[i+1]=="Pa"):
#             words.append(word_list)
#             word_list.clear()
#             continue
#         word_list.append(swara_list[i])
#     return plaintext

# Example usage
plaintext = "Knowledge is power"
raga = "Mayamalavagowla"
ciphertext = encrypt(plaintext, alphabet_swara_Mayamalavagowla)
print("Ciphertext:", ciphertext)
freq_list = generate_freqency_list(ciphertext)
print(freq_list,len(freq_list))

sampling_rate=44100
music = generate_audio_sequence(freq_list)
audio_file = "audio_sequence.wav"  # Replace with your audio file path
duration=0.5
window_size = int(duration * sampling_rate)  # Window size for FFT (0.5 seconds)
overlap = 0
swara_list = get_frequency_list(audio_file, window_size, overlap,swara_freq)
# print(swara_list)
# decrypted_text = decrypt_swara(swara_list, alphabet_swara_Mayamalavagowla)
# print("Decrypted text:", decrypted_text)