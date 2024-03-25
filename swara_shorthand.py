# Table I: Swara-Frequency Mapping
swara_freq = {
    'Sa': 260.29, 'Ri1': 277.84, 'Ri2, Ga1': 293.08, 'Ri3, Ga2': 309.66,
    'Ga3': 330.28, 'Ma1': 346.90, 'Ma2': 372.19, 'Pa': 390.61,
    'Dha1': 414.82, 'Dha2, Ni1': 440.00, 'Dha3, Ni2': 462.33, 'Ni3': 495.84
}

ragas = {
    "Mayamalavagowla": {
        "arohana": "Sa Ri1 Ga3 Ma1 Pa Dha1 Ni3 Sa",
        "amsa_swara": "Pa"
    }
}

# Given list of swaras
swaras = ['Ri', 'Ma', 'Dha', 'Pa', 'Ga', 'Dha', 'Pa', 'Ga', 'Ma', 'Pa', 'Ma', 'Dha', 'Ni', 'Pa', 'Sa', 'Ni', 'Pa', 'Dha', 'Ni', 'Pa', 'Ri', 'Ga', 'Pa', 'Ga', 'Ma', 'Ni', 'Pa', 'Dha', 'Ni', 'Pa', 'Pa', 'Ga', 'Ni', 'Pa', 'Ri', 'Ni', 'Pa', 'Pa', 'Ga', 'Ma', 'Dha', 'Pa', 'Ga', 'Ma', 'Pa', 'Ma', 'Dha', 'Ni', 'Pa', 'Dha', 'Ni', 'Pa', 'Ri', 'Ma', 'Pa', 'Pa']

# Function to map shorthand swaras to full swaras
def map_shorthand_swaras(swaras):
    full_swaras = []
    for swara in swaras:
        if swara == 'Ri':
            full_swaras.append('Ri1')
        elif swara == 'Ga':
            full_swaras.append('Ga3')
        elif swara == 'Dha':
            full_swaras.append('Dha1')
        elif swara == 'Ni':
            full_swaras.append('Ni3')
        else:
            full_swaras.append(swara)
    return full_swaras

# Function to calculate frequency based on given swaras and their frequencies
def calculate_frequency(swaras):
    frequencies = {}
    for swara in swaras:
        frequencies[swara] = swara_freq[swara]
    return frequencies

# Mapping shorthand swaras to full swaras
full_swaras = map_shorthand_swaras(swaras)

# Calculating frequency of each swara
frequencies = calculate_frequency(full_swaras)

# Outputting the frequencies
print("Frequency of each swara:")
for swara, freq in frequencies.items():
    print(f"{swara}: {freq} Hz")
