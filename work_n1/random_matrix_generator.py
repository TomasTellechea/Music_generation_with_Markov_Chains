import random


def generate_transition_matrix(rows, cols):
    transition_matrix = []
    for _ in range(rows):
        row = [0] * cols
        # Selecciona aleatoriamente 3 posiciones únicas
        positions = random.sample(range(cols), 3)
        row[positions[0]] = 0.2
        row[positions[1]] = 0.2
        row[positions[2]] = 0.6
        transition_matrix.append(row)
    return transition_matrix


rows = 12
cols = 12
transition_matrix = generate_transition_matrix(rows, cols)

for row in transition_matrix:
    print(f'{row},')
