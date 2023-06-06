import random
from networkx import Graph, draw
import matplotlib.pyplot as plt
import networkx as nx


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


# sprawdzanie hybrydyzacji
def check_hybridization(seq1, seq2):
    if len(seq1) != len(seq2):
        return False

    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    for i in range(len(seq1)):
        if complement[seq1[i]] != seq2[i]:
            return False

    return True

def gen_weight(str1, str2):
    for x in range(len(str1)):
        if str2.startswith(str1[0+x:len(str1)]):
            return len(str1[0+x:len(str1)])
    return 0

dna_sequence = generate_dna_sequence(10)
ordered_subsequences = generate_subsequences(dna_sequence, 7)

# Wymieszanie elementów spektrum
shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))

# print(dna_sequence)
# print(ordered_subsequences)
# print(shuffled_subsequences)

sequence1 = ordered_subsequences[0]
sequence2 = shuffled_subsequences[0]

# if check_hybridization(sequence1, sequence2):
#     print("Sekwencje hybrydyzują ze sobą.")
# else:
#     print("Sekwencje nie hybrydyzują ze sobą.")

# Tworzenie pustego grafu
graph = nx.Graph()

# Dodawanie wierzchołków do grafu
graph.add_nodes_from(shuffled_subsequences)

# Dodawanie krawędzi między wierzchołkami
for i in range(len(shuffled_subsequences)):
    for j in range(i + 1, len(shuffled_subsequences)):
        # waga krawędzi = długość_oligonukleotydów – liczba_liter_ich_nałożenia
        similarity = len(shuffled_subsequences[i]) - gen_weight(shuffled_subsequences[i], shuffled_subsequences[j])
        graph.add_edge(shuffled_subsequences[i], shuffled_subsequences[j], weight=similarity)


# Rysowanie grafu
pos = nx.circular_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')

# Rysowanie etykiet wag na krawędziach
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

# Wyświetlanie grafu
plt.show()

print(shuffled_subsequences[0])
print(shuffled_subsequences[1])
# # Wyświetlanie informacji o grafie
# print("Wierzchołki grafu:", graph.nodes())
# print("Krawędzie grafu:", graph.edges())

