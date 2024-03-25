import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read

# Define the sampling frequency
sampling_freq = 44100

# Define the duration of each character
char_duration = 0.5  # in seconds

# Define the lookup table for each letter (assuming lowercase)
lookup_table = {
    'a': 440, 'b': 494, 'c': 523, 'd': 587, 'e': 659, 'f': 698, 'g': 784,
    'h': 880, 'i': 988, 'j': 1047, 'k': 1175, 'l': 1319, 'm': 1397, 'n': 1760,
    'o': 1528, 'p': 1976, 'q': 2093, 'r': 2349, 's': 2637, 't': 2794, 'u': 3136,
    'v': 3520, 'w': 3951, 'x': 4186, 'y': 4699, 'z': 5274
}

def generate_audio(letter):
    duration = int(sampling_freq * char_duration)
    t = np.linspace(0, char_duration, duration)
    frequency = lookup_table[letter.lower()]
    audio_data = np.sin(2 * np.pi * frequency * t)
    return audio_data

def text_to_audio(text):
    audio_data = np.array([])
    for char in text:
        if char.lower() in lookup_table:
            audio_data = np.append(audio_data, generate_audio(char))
    write('output.wav', sampling_freq, np.int16(audio_data * 32767))

text_to_audio("Knowledge is power")
print("34")

def audio_to_text(audio_file):
    sampling_freq, audio_data = read(audio_file)
    text = ""
    for sample in audio_data:
        for letter, frequency in lookup_table.items():
            if np.array_equal(sample, generate_audio(letter)):
                text += letter
                break
    return text

# Example usage
print(audio_to_text('output.wav'))
