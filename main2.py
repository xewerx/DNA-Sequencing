import random
from networkx import Graph, draw
import matplotlib.pyplot as plt
import networkx as nx
import os
import re
import time


#STALE:
N = 100
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

def save_sequence_to_file(sequence, folder, filename):
    # Tworzenie ścieżki do folderu
    folder_path = os.path.join(os.getcwd(), folder)

    # Sprawdzanie istnienia folderu
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Tworzenie ścieżki do pliku
    file_path = os.path.join(folder_path, filename)

    with open(filename, 'w') as file:
        file.write(sequence)


def save_subsequences_to_file(subsequences, folder, filename):
    # Tworzenie ścieżki do folderu
    folder_path = os.path.join(os.getcwd(), folder)

    # Sprawdzanie istnienia folderu
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Tworzenie ścieżki do pliku
    file_path = os.path.join(folder_path, filename)

    # Zapisywanie danych do pliku
    with open(file_path, 'w') as file:
        for subsequence in subsequences:
            file.write(subsequence + '\n')


dna_sequence = generate_dna_sequence(N)
ordered_subsequences = generate_subsequences(dna_sequence, K)
shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))

save_sequence_to_file(dna_sequence, 'input', 'dane.txt')
save_subsequences_to_file(shuffled_subsequences, 'input', 'sequences.txt')



def read_file(filename):
    nodes = []
    with open(filename) as f:
        lines = f.readlines()
    for idx, i in enumerate(lines):
        value = i.replace('\n', '')
        nodes.append(Node(value, idx))

    paths = [[Path(0, 1) for _ in range(len(nodes))] for _ in range(len(nodes))]

    return nodes, paths


def set_lengths(nodes, paths):
    for y, node_y in enumerate(nodes):
        for x, node_x in enumerate(nodes):
            if x != y:
                value = node_y.set_distance(node_x)
                paths[y][x].length = value
    return paths


class Ant:
    def __init__(self, max_words, start):
        self.max_words = max_words
        self.current = start
        self.road = []
        self.result = 1
        self.running = True

    def travel_road(self, paths, nodes):
        global best_result
        global best_path
        while self.running:
            potential_nodes = []
            self.road.append(self.current)
            for i in nodes:
                if i == self.current:
                    continue
                if self.current.get_path(i, paths).length <= self.max_words and i not in self.road:
                    potential_nodes.append(i)
            if not potential_nodes:
                self.running = False
            if not self.running:
                break
            possibilities = [
                pow(self.current.get_path(i, paths).pheromone, alfa) / pow(self.current.get_path(i, paths).length, beta)
                for i in potential_nodes]
            choice = random.choices(potential_nodes, possibilities)[0]
            self.result += 1
            self.max_words -= self.current.get_path(choice, paths).length
            self.current = choice

        prev_node = None
        for temporary_node in potential_nodes:
            if prev_node is None:
                prev_node = temporary_node
                continue
            temporary_path = temporary_node.get_path(prev_node, paths)
            temporary_path.add_pheromone(self.result)
            prev_node = temporary_node

        if self.result >= best_result and n - len(self.road) <= n - len(best_path):
            best_path = self.road
            best_result = self.result




class AntColony:
    def __init__(self, ants, iteration):
        self.iteration = iteration
        self.ants = ants

    def launch(self, paths, nodes):
        for i in range(self.iteration):
            print("iteration:", i + 1)
            for ant in range(self.ants):
                # print("ant:", ant + 1)
                temp = Ant(n, nodes[random.randint(0, len(nodes) - 1)])
                temp.travel_road(paths, nodes)
            self.release_pheromones(paths)

    def release_pheromones(self, paths):
        for path in paths:
            for x in path:
                x.evaporate_pheromone()


class Node:
    def __init__(self, value, id):
        self.value = value
        self.id = id

    def set_distance(self, other):
        for i in range(len(self.value)):
            if self.value[i:] == other.value[:len(other.value) - i]:
                return i
        return len(self.value)

    def get_path(self, other, paths):
        return paths[self.id][other.id]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Path:
    def __init__(self, length, pheromone):
        self.length = length
        self.pheromone = pheromone

    def evaporate_pheromone(self):
        self.pheromone *= (1 / p)

    def add_pheromone(self, result):
        self.pheromone += result * Q

    def __str__(self):
        return str(self.length, self.pheromone)

    def __repr__(self):
        return str(self.length, self.pheromone)


def convert_to_strings(node_list):
    string_list = []
    for node in node_list:
        string_list.append(node.value)
    return string_list


def merge_strings(string_list):
    merged_string = string_list[0]  # Początkowa wartość - pierwszy element tablicy

    for i in range(1, len(string_list)):
        current_string = string_list[i]

        # Sprawdzanie powtarzających się znaków na końcu poprzedniego stringa
        common_suffix = ""
        for j in range(1, min(len(merged_string), len(current_string)) + 1):
            if merged_string[-j:] == current_string[:j]:
                common_suffix = merged_string[-j:]

        # Usuwanie powtarzających się znaków
        merged_string = merged_string + current_string[len(common_suffix):]

    return merged_string


def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    # Inicjalizacja tablicy o rozmiarze (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inicjalizacja pierwszego wiersza i pierwszej kolumny
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Wypełnianie tablicy dynamicznego programowania
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

if __name__ == "__main__":

    p = 0.7  #
    Q = 0.7  #
    alfa = 1  #
    beta = 5  #
    ants_number = 30
    iterations_number = 10

    best_path = []
    best_result = 0

    n = N
    nodes, paths = read_file('input/sequences.txt')

    set_lengths(nodes, paths)

    start_time = time.time()

    colony = AntColony(ants_number, iterations_number)
    colony.launch(paths, nodes)

    colony_dna_sequence_best_path = ''

    final_length = sum(node.get_path(best_path[i + 1], paths).length for i, node in enumerate(best_path[:-1]))

    end_time = time.time()
    execution_time = end_time - start_time

    result = [best_path[0]]  # Inicjalizacja wynikowej tablicy z pierwszym wierzchołkiem


    string_list = convert_to_strings(best_path)

    colony_dna_sequence_best_path = merge_strings(string_list)

    with open('dane.txt', 'r') as file:
        string1 = file.read()

    # print(string1)

    distance = levenshtein_distance(string1, colony_dna_sequence_best_path)
    lewenstein_value = (distance / (max(len(colony_dna_sequence_best_path), len(string1)))) * 100


    print("Final length:", final_length)
    print("Number of words (odwiedzone wierzcholki) :", len(best_path))
    print("Execution time:", execution_time, "seconds")
    print("Best road:", best_path)
    print("pokrycie grafu: odwiedzone wiezcholki/ilosc wierzchołków :", ((len(best_path)/(n-K+1))*100), "%")
    print("DNA wejściowe (z pliku dane.txt) : ", string1)
    print("colony_dna_sequence_best_path:", colony_dna_sequence_best_path)
    print("Miara lewensteina:", lewenstein_value , "%")

    with open(f"output.txt", "w") as f:
        f.write("Final length: " + str(final_length) + '\n')
        f.write("Number of words:" + str(len(best_path)) + '\n')
        f.write("Execution time:" + str(execution_time) + "seconds" + '\n')
        f.write("Best road  (odwiedzone wierzcholki) : " + str(best_path) + '\n')
        f.write("p:" + str(p) + '\n')
        f.write("Q:" + str(Q) + '\n')
        f.write("alfa:" + str(alfa) + '\n')
        f.write("beta:" + str(beta) + '\n')
        f.write("ants number:" + str(ants_number) + '\n')
        f.write("iterations number:" + str(iterations_number) + '\n')
        f.write("pokrycie grafu: (odwiedzone wiezcholki/ilosc wierzcholkow) :" + str(((len(best_path) / (n - K + 1)) * 100)) + "%" + '\n')
        f.write("Miara lewensteina:" + str(lewenstein_value) + "%" + '\n')
