import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write


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

def map_shorthand_swaras(swaras):
    shorthand_to_full = {
        'Ri': 'Ri1',
        'Ga': 'Ga3',
        'Ma': 'Ma1',
        'Dha': 'Dha1',
        'Ni': 'Ni3'
    }
    return [shorthand_to_full.get(swara, swara) for swara in swaras]

def reverse_map_full_swaras(full_swaras):
    full_to_shorthand = {
        'Ri1': 'Ri',
        'Ga3': 'Ga',
        'Ma1': 'Ma',
        'Dha1': 'Dha',
        'Ni3': 'Ni'
    }
    return [full_to_shorthand.get(swara, swara) for swara in full_swaras]


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


def generate_audio_sequence(frequency_list, duration=0.5, sampling_rate=44100, output_wav="audio_sequence.wav", output_midi="audio_sequence.mid"):
    """
    Generate an audio sequence based on a list of frequencies and write it to a WAV file and a MIDI file.

    Parameters:
        frequency_list (list): List of frequencies for each tone.
        duration (float): Duration of each tone in seconds. Defaults to 0.5 seconds.
        sampling_rate (int): Sampling rate in Hz. Defaults to 44100 Hz.
        output_wav (str): Output file path for the generated WAV file. Defaults to "audio_sequence.wav".
        output_midi (str): Output file path for the generated MIDI file. Defaults to "audio_sequence.mid".

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
    write(output_wav, sampling_rate, audio_sequence)

    # Create a MIDI file
    midi_file = mido.MidiFile()
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    # Set tempo and time signature
    tempo = mido.bpm2tempo(120)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))

    # Add notes to the MIDI track
    for freq in frequency_list:
        note = mido.Message('note_on', note=midi_note_number(freq), velocity=100, time=0)
        track.append(note)
        note = mido.Message('note_off', note=midi_note_number(freq), velocity=100, time=int(mido.second2tick(duration, midi_file.ticks_per_beat, tempo)))
        track.append(note)

    # Save the MIDI file
    midi_file.save(output_midi)

def midi_note_number(frequency):
    """
    Convert frequency to MIDI note number.

    Parameters:
        frequency (float): Frequency in Hz.

    Returns:
        int: MIDI note number.
    """
    return int(12 * np.log2(frequency / 440) + 69)

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
    return reverse_map_full_swaras(nearest_swara)

def decrypt_swara(swara_list):
    plaintext = ''
    words=[]
    word_list = []
    for i in range(len(swara_list)-1):
        if(swara_list[i]=="Pa" and swara_list[i-1]=="Pa"):
            continue
        if(swara_list[i]=="Pa" and swara_list[i+1]=="Pa"):
            # print(word_list)
            words.append(word_list.copy())
            word_list.clear()
            continue
        word_list.append(swara_list[i])
    list_of_strings=[]
    for word in words:
        characters=[]
        swara_subseq=''
        for i in range(len(word)):
            if word[i] == "Pa":
                swara_subseq= swara_subseq[:-1]+"Pa"
                continue
            swara_subseq+=word[i] + " "
        # print(swara_subseq)
        list_of_strings.append(swara_subseq)
    single_string=''
    for string in list_of_strings:
        single_string +=string[:-1] + "Pa Pa"
    return single_string[:-5]+"Pa"

# Example usage
plaintext = "Knowledge is power"
print(plaintext)
raga = "Mayamalavagowla"
ciphertext = encrypt(plaintext, alphabet_swara_Mayamalavagowla)
print("Ciphertext:", ciphertext)
freq_list = generate_freqency_list(ciphertext)

sampling_rate=44100
music = generate_audio_sequence(freq_list)


audio_file = "audio_sequence.wav"  # Replace with your audio file path
duration=0.5
window_size = int(duration * sampling_rate)  # Window size for FFT (0.5 seconds)
overlap = 0
swara_list = get_frequency_list(audio_file, window_size, overlap,swara_freq)

decrypted_cypher = decrypt_swara(swara_list)
print(decrypted_cypher)
decrypted_text = decrypt_ciphertext(decrypted_cypher,alphabet_swara_Mayamalavagowla)
print("Decrypted text:", decrypted_text)