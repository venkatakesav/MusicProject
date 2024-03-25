import sys

# Raga definitions
ragas = {
    "Mayamalavagowla": {
        "arohana": "Sa Ri1 Ga3 Ma1 Pa Dha1 Ni3 Sa",
        "amsa_swara": "Pa"
    },
    "Shankarabharana": {
        "arohana": "Sa Ri2 Ga3 Ma1 Pa Dha2 Ni3 Sa",
        "amsa_swara": "Pa"
    },
    "Kharaharapriya": {
        "arohana": "Ri2 Ga1 Ma1 Pa Dha2 Ni1 Sa",
        "amsa_swara": "Pa"
    },
    "Kalyani": {
        "arohana": "Sa Ri2 Ga3 Ma2 Pa Dha2 Ni3 Sa",
        "amsa_swara": "Pa"
    },
    "Harikambhoji": {
        "arohana": "Sa Ri2 Ga2 Ma1 Pa Dha2 Ni1 Sa",
        "amsa_swara": "Ma"
    },
    "Mohanam": {
        "arohana": "Sa Ri1 Ga2 Ma1 Pa Dha1 Ni1 Sa",
        "amsa_swara": "Pa"
    },
    "Bhairavi": {
        "arohana": "Sa Ri1 Ga1 Ma1 Pa Dha1 Ni1 Sa",
        "amsa_swara": "Pa"
    },
    "Hindolam": {
        "arohana": "Sa Ri1 Ga3 Ma1 Pa Dha2 Ni3 Sa",
        "amsa_swara": "Pa"
    },
    "Sankarabharanam": {
        "arohana": "Sa Ri2 Ga3 Ma1 Pa Dha2 Ni3 Sa",
        "amsa_swara": "Pa"
    },
    "Keeravani": {
        "arohana": "Sa Ri1 Ga2 Ma1 Pa Dha2 Ni1 Sa",
        "amsa_swara": "Pa"
    }
}

def generate_lookup_table(raga):
    arohana = ragas[raga]["arohana"].split()
    amsa_swara = ragas[raga]["amsa_swara"]
    lookup_table = {}

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char == " ":
            lookup_table[char] = "Pa"
        else:
            swara_sequence = []
            for swara in arohana:
                if swara != amsa_swara:
                    if char in lookup_table.values():
                        swara_sequence.append(swara)
                    if len(swara_sequence) == 2 or len(swara_sequence) == 3:
                        break
            lookup_table[char] = "".join(swara_sequence)

    return lookup_table

if __name__ == "__main__":
    print("Available Ragas:")
    for raga in ragas:
        print(f"- {raga}")

    selected_raga = input("Enter the raga (case-sensitive): ")
    if selected_raga in ragas:
        lookup_table = generate_lookup_table(selected_raga)
        print(f"\nLookup Table for Raga {selected_raga}:")
        for char, swara_sequence in lookup_table.items():
            print(f"{char} - {swara_sequence}")
    else:
        print(f"Error: Raga '{selected_raga}' not found.")
        sys.exit(1)