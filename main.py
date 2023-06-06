#TODO: whole project :D

import random

#stworzenie nitki DNA
def generate_dna_sequence(length):
    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ''

    for _ in range(length):
        nucleotide = random.choice(nucleotides)
        sequence += nucleotide

    return sequence

#Tworzymy zbiór oligonukleotydów
def generate_subsequences(sequence, k):
    subsequences = []
    for i in range(len(sequence) - k + 1):
        subsequence = sequence[i:i+k]
        subsequences.append(subsequence)
    return subsequences

#sprawdzanie hybrydyzacji
def check_hybridization(seq1, seq2):
    if len(seq1) != len(seq2):
        return False

    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    for i in range(len(seq1)):
        if complement[seq1[i]] != seq2[i]:
            return False

    return True


dna_sequence = generate_dna_sequence(700)
ordered_subsequences = generate_subsequences(dna_sequence, 7)

#Wymieszanie elementów spektrum
shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))

print(dna_sequence)
print(ordered_subsequences)
print(shuffled_subsequences)

sequence1 = ordered_subsequences[0]
sequence2 = shuffled_subsequences[0]

if check_hybridization(sequence1, sequence2):
    print("Sekwencje hybrydyzują ze sobą.")
else:
    print("Sekwencje nie hybrydyzują ze sobą.")

