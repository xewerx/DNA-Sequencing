import random
import time

from generator import create_errors, generate_dna_sequence, generate_subsequences, save_sequence_to_file, save_subsequences_to_file
from get_levenshtein_distance import levenshtein_distance

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

        if self.result >= best_result and N - len(self.road) <= N - len(best_path):
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
                temp = Ant(N, nodes[random.randint(0, len(nodes) - 1)]) # mrówka startuje z losowego wierzchołka
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

    def get_distance(self, other):
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
        self.pheromone *= (1 / rho)

    def add_pheromone(self, result):
        self.pheromone += result * Q

    def __str__(self):
        return str(self.length, self.pheromone)

    def __repr__(self):
        return str(self.length, self.pheromone)


def read_file(filename):
    nodes = []
    with open(filename) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        value = line.replace('\n', '')
        nodes.append(Node(value, i))

    paths = [[Path(0, 1) for _ in range(len(nodes))] for _ in range(len(nodes))]

    return nodes, paths


def set_weights(nodes, paths):
    for y, node_y in enumerate(nodes):
        for x, node_x in enumerate(nodes):
            if x != y:
                value = node_y.get_distance(node_x)
                paths[y][x].length = value
    return paths

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

if __name__ == "__main__":
    # stałe
    N = 100
    K = 7

    # generowanie danych
    dna_sequence = generate_dna_sequence(N)
    ordered_subsequences = generate_subsequences(dna_sequence, K)
    shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))
    shuffled_subsequences_with_errors = create_errors(shuffled_subsequences, 10, 15)
    save_sequence_to_file(dna_sequence, 'input', 'dane.txt')
    save_subsequences_to_file(shuffled_subsequences_with_errors, 'input', 'sequences.txt')
    
    # uruchomienie ACO
    rho = 0.7
    Q = 0.7
    alfa = 0.7
    beta = 5
    colony_size = 30
    steps = 5

    best_path = []
    best_result = 0

    nodes, paths = read_file('input/sequences.txt')

    set_weights(nodes, paths)

    start_time = time.time()

    colony = AntColony(colony_size, steps)
    colony.launch(paths, nodes)
    
    final_length = sum(node.get_path(best_path[i + 1], paths).length for i, node in enumerate(best_path[:-1]))

    string_list = convert_to_strings(best_path)

    colony_dna_sequence_best_path = merge_strings(string_list)

    with open('input/dane.txt', 'r') as file:
        original_dna = file.read()

    distance = levenshtein_distance(original_dna, colony_dna_sequence_best_path)
    levenshtein_value = (distance / (max(len(colony_dna_sequence_best_path), len(original_dna)))) * 100
    
    end_time = time.time()
    execution_time = end_time - start_time

    with open(f"output/output.txt", "w") as f:
        f.write("Final length: " + str(final_length) + '\n')
        f.write("Number of words: " + str(len(best_path)) + '\n')
        f.write("Execution time: " + str(execution_time) + "seconds" + '\n')
        f.write("Best road  (odwiedzone wierzcholki): " + str(best_path) + '\n')
        f.write("rho: " + str(rho) + '\n')
        f.write("Q: " + str(Q) + '\n')
        f.write("alfa: " + str(alfa) + '\n')
        f.write("beta: " + str(beta) + '\n')
        f.write("Liczba mrowek: " + str(colony_size) + '\n')
        f.write("Liczba krokow:"  + str(steps) + '\n')
        f.write("Pokrycie grafu: (odwiedzone wiezcholki/ilosc wierzcholkow): " + str(((len(best_path) / (N - K + 1)) * 100)) + "%" + '\n')
        f.write("DNA wejsciowe (z pliku dane.txt): " + original_dna + '\n')
        f.write("colony_dna_sequence_best_path: " + colony_dna_sequence_best_path + '\n')
        f.write("Miara Vewensteina: " + str(levenshtein_value) + "%" + '\n')