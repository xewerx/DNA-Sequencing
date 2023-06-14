import os
import random

from constatnts import K

# stworzenie nitki DNA
def generate_dna_sequence(length):
    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ''

    for _ in range(length):
        nucleotide = random.choice(nucleotides)
        sequence += nucleotide

    return sequence

# tworzymy zbiór oligonukleotydów
def generate_subsequences(sequence, k):
    subsequences = []
    for i in range(len(sequence) - k + 1):
        subsequence = sequence[i:i + k]
        subsequences.append(subsequence)
    return subsequences

def create_errors(subsequences, negative, positive):
    sequence_with_errors = subsequences
    if negative > 0:
        sequence_with_errors = subsequences[0:len(subsequences) - negative]
    if positive > 0:
        sequence_with_errors = sequence_with_errors + [generate_dna_sequence(K) for _ in range(positive)]
    return sequence_with_errors


def save_sequence_to_file(sequence, folder, filename):
    folder_path = os.path.join(os.getcwd(), folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w') as file:
        file.write(sequence)


def save_subsequences_to_file(subsequences, folder, filename):
    folder_path = os.path.join(os.getcwd(), folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w') as file:
        for subsequence in subsequences:
            file.write(subsequence + '\n')

def read_sequence_from_file(file_path):
    with open(file_path) as f:
        sequence = f.readlines()
    return sequence

def read_subsequences_from_file(file_path):
    subsequences = []
    with open(file_path) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        value = line.replace('\n', '')
        subsequences.append(value)

    return subsequences