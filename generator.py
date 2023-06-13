import random

# stworzenie nitki DNA
def generate_dna_sequence(length):
    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ''

    for _ in range(length):
        nucleotide = random.choice(nucleotides)
        sequence += nucleotide

    return sequence

# Tworzymy zbiór oligonukleotydów
def generate_subsequences(sequence, k):
    subsequences = []
    for i in range(len(sequence) - k + 1):
        subsequence = sequence[i:i + k]
        subsequences.append(subsequence)
    return subsequences


K = 10
N = 100
dna_sequence = generate_dna_sequence(N)
ordered_subsequences = generate_subsequences(dna_sequence, K)

# Wymieszanie elementów spektrum
shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))

with open(f"data.txt", "w") as f:
    for subsequence in shuffled_subsequences:
        f.write(subsequence + '\n')