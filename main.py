import random
from networkx import Graph, draw
import matplotlib.pyplot as plt
import networkx as nx

#STALE:
N = 14
K = 7

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

#obliczanie wag na krawędziach grafu
def gen_weight(str1, str2):
    weight = 0
    for i in range(1, len(str1)):
        if str1[:i] == str2[-i:]:
            weight = i
        if str2[:i] == str1[-i:]:
            weight = i
    return weight


# def gen_weight(str1, str2):
#     for x in range(len(str1)):
#         if str2.startswith(str1[0+x:len(str1)]):
#             return len(str1[0+x:len(str1)])
#     return 0

dna_sequence = generate_dna_sequence(N)
ordered_subsequences = generate_subsequences(dna_sequence, K)

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
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels,label_pos=0.75)

# Wyświetlanie grafu


print(shuffled_subsequences[0])
print(shuffled_subsequences[1])

# # #  ---------------------------  Wyświetlanie grafu -----------------------
# plt.show()

# # Wyświetlanie informacji o grafie
# print("Wierzchołki grafu:", graph.nodes())
# print("Krawędzie grafu:", graph.edges())


# #  ---------------------------  Algorytm zachłanny -----------------------

# Funkcja pomocnicza do wybierania wierzchołka o najniższej wadze krawędzi
def get_next_node(current_node):
    min_weight = float('inf')
    next_node = None

    for neighbor in graph.neighbors(current_node):
        weight = graph.edges[current_node, neighbor]['weight']
        if neighbor not in visited_nodes and weight < min_weight:
            min_weight = weight
            next_node = neighbor

    return next_node


# Lista odwiedzonych wierzchołków
visited_nodes = []
# Inicjalizacja sumy znaków
total_chars = 0
# Rozpoczęcie od wierzchołka shuffled_subsequences[0]
start_node = shuffled_subsequences[0]

# Algorytm zachłanny
current_node = start_node
visited_nodes.append(current_node)

# while total_chars < N:
#     next_node = get_next_node(current_node)
#
#     # Jeśli nie ma więcej sąsiadów do odwiedzenia, przerwij pętlę
#     if next_node is None:
#         break
#
#     weight = graph.edges[current_node, next_node]['weight']
#     unique_chars = set(next_node) - set(current_node)
#
#     if not unique_chars:
#         break
#     # Dodanie wierzchołka do odwiedzonych i aktualizacja bieżącego wierzchołka
#     visited_nodes.append(next_node)
#     total_chars += weight
#
#     current_node = next_node

# Pętla zachłanna
while len(visited_nodes) < len(graph.nodes):
    min_weight = float('inf')
    next_node = None

    # Wybór wierzchołka o najniższej wadze krawędzi
    for neighbor in graph.neighbors(current_node):
        weight = graph.edges[current_node, neighbor]['weight']
        if weight < min_weight and neighbor not in visited_nodes:
            min_weight = weight
            next_node = neighbor

    # Jeśli nie ma więcej sąsiadów do odwiedzenia, przerwij pętlę
    if next_node is None:
        break

    # Dodanie wierzchołka do odwiedzonych i aktualizacja bieżącego wierzchołka
    visited_nodes.append(next_node)
    current_node = next_node

# Wyświetlenie odwiedzonych wierzchołków
print(ordered_subsequences)
print(shuffled_subsequences)
print("Odwiedzone wierzchołki:", visited_nodes)

plt.show()
