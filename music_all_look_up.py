import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import json
import mido

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

def map_shorthand_swaras(swaras,raga_seq):
    for i,swara in enumerate(swaras):
        #get index of substring swara in raga_seq
        index = raga_seq.find(swara)
        if(swara!="Pa" and swara!="Dha" and swara!="Sa"):
            num = raga_seq[index+2:index+3]
            swaras[i] = swara+num
        elif(swara=="Dha"):    
            num = raga_seq[index+3:index+4]
            swaras[i] = swara+num
    return swaras
    shorthand_to_full = {
        'Ri': 'Ri1',
        'Ga': 'Ga3',
        'Ma': 'Ma1',
        'Dha': 'Dha1',
        'Ni': 'Ni3'
    }
    return [shorthand_to_full.get(swara, swara) for swara in swaras]

def reverse_map_full_swaras(full_swaras):
    for (i,swara) in enumerate(full_swaras):
        if(len(swara))==3:
            full_swaras[i]=swara[:2]
        elif(len(swara))==4:
            full_swaras[i]=swara[:3]
    return full_swaras
    full_to_shorthand = {
        'Ri1': 'Ri',
        'Ga3': 'Ga',
        'Ma1': 'Ma',
        'Dha1': 'Dha',
        'Ni3': 'Ni'
    }
    return [full_to_shorthand.get(swara, swara) for swara in full_swaras]


# Music generation
def generate_freqency_list(swara_sequence,raga_seq):
    swara_list = []
    for word in swara_sequence.split('Pa Pa'):
        for character in word.split("Pa"):
            if(character != ""):
                swara_list.extend(character.split())
                swara_list.extend("Pa".split())
        swara_list.extend("Pa".split())
    swara_list = map_shorthand_swaras(swara_list,raga_seq)
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

def generate_audio_sequence(frequency_list, duration=0.5, sampling_rate=44100, output_file="audio_sequence.wav", output_midi="audio_sequence.mid"):
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
    output_wav = output_file
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

def scoring(audio_file):
    score = random.randint(0,100)
    return score

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

def best_look_up_table(look_up_tables,plaintext):
    max_score = 0
    best_look_up_table = None
    a=0
    for look_up_table in look_up_tables:
        alphabet_swara = look_up_table
        ciphertext = encrypt(plaintext, alphabet_swara)
        freq_list = generate_freqency_list(ciphertext,arohana_swara[raga])
        audio_file = "./midi_files/audio_sequence.wav"
        sampling_rate=4000
        duration=0.25
        music = generate_audio_sequence(freq_list,duration=duration,sampling_rate=sampling_rate,output_file=audio_file,output_midi=f"./midi_files/audio_sequence_{a}.mid")
        a+=1

    for i in range(a):
        audio_file = f"./midi_files/audio_sequence_{i}.mid"
        score = scoring(audio_file)
        if score > max_score:
            max_score = score
            best_look_up_table = look_up_tables[i]
    return best_look_up_table
# Example usage

# Table I: Swara-Frequency Mapping
with open("swara_freq.json","r") as f:
    swara_freq = json.load(f)

# Table II: Plaintext Alphabet-Swara Sequence Mapping
with open("arohan_swara.json","r") as f:
    arohana_swara = json.load(f)

with open("two_three_four_five_comb.json","r") as f:
    two_three_four_five_comb = json.load(f)

raga="mayamalavagowla"
amsa_swara = "Pa"

plaintext = "Knowledge is power"
print(plaintext)

# Encryption
all_possible_two_comb = two_three_four_five_comb[0]
all_possible_three_comb = two_three_four_five_comb[1]
import random
random_two_list=[]
for i in range(10):
    random_two_list.append(random.sample(range(15),15))
random_three_list=[]
for i in range(10):
    random_three_list.append(random.sample(range(11),11))
look_up_tables = []
two_list = ['A', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'R', 'S', 'T', 'U']
three_list = ['B', 'G', 'J', 'K', 'P', 'Q', 'V', 'W', 'X', 'Y', 'Z']
for i in range(10):
    look_up_table = {}
    for j in range(15):
        look_up_table[two_list[j]]=" ".join(all_possible_two_comb[random_two_list[i][j]])
    for j in range(11):
        look_up_table[three_list[j]]=" ".join(all_possible_three_comb[random_three_list[i][j]])
    # print(look_up_table)
    look_up_tables.append(look_up_table)


alphabet_swara = best_look_up_table(look_up_tables,plaintext)
# now look_up_tables contains 10 look up tables

ciphertext = encrypt(plaintext, alphabet_swara)
print("Ciphertext:", ciphertext)


freq_list = generate_freqency_list(ciphertext,arohana_swara[raga])
print(raga)

audio_file = "audio_sequence.wav"
sampling_rate=4000
duration=0.25
music = generate_audio_sequence(freq_list,duration=duration,sampling_rate=sampling_rate,output_file=audio_file)


# Decryption
audio_file = "audio_sequence.wav"  # Replace with your audio file path
sampling_rate=4000
duration=0.25
window_size = int(duration * sampling_rate)  # Window size for FFT (0.5 seconds)
overlap = 0
swara_list = get_frequency_list(audio_file, window_size, overlap,swara_freq)

decrypted_cypher = decrypt_swara(swara_list)
print(decrypted_cypher)

decrypted_text = decrypt_ciphertext(decrypted_cypher,alphabet_swara)
print("Decrypted text:", decrypted_text)