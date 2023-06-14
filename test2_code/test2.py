# generowanie danych
import random
from constatnts import K, N
from generator import create_errors, generate_dna_sequence, generate_subsequences, read_sequence_from_file, read_subsequences_from_file, save_sequence_to_file, save_subsequences_to_file

errors_percentages = [2, 4, 6, 8, 10]

for i in range(20):
    dna_sequence = generate_dna_sequence(N)
    ordered_subsequences = generate_subsequences(dna_sequence, K)
    shuffled_subsequences = random.sample(ordered_subsequences, len(ordered_subsequences))
    save_sequence_to_file(dna_sequence, 'test2_data/no_errors', f'dna_{i}.txt')
    save_subsequences_to_file(shuffled_subsequences, 'test2_data/no_errors', f'sequences_{i}.txt')


    for errors_percentage_i, errors_percentage in enumerate(errors_percentages):
        # sequence = read_sequence_from_file(f'test2_data/no_errors/dna_{i}.txt')[0]
        subsequences = read_subsequences_from_file(f'test2_data/no_errors/sequences_{i}.txt')
        subsequences_with_errors = create_errors(subsequences, int((N - K + 1) * 0.01 * errors_percentage), 0)
        print(len(subsequences_with_errors))
        save_subsequences_to_file(subsequences_with_errors, f'test2_data/{errors_percentage}_errors', f'sequences_{i}.txt')