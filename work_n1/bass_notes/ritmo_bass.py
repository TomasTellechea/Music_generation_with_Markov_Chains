import numpy as np
from music21 import *
import pickle


class MarkovChainRhythmGenerator:
    def __init__(self, rhythms, initial_probabilities, transition_matrix):
        self.rhythms = rhythms
        self.initial_probabilities = np.array(initial_probabilities)
        self.transition_matrix = np.array(transition_matrix)
        self._rhythm_indexes = {rhythm: i for i, rhythm in enumerate(rhythms)}

    def generate(self, length):
        rhythm_sequence = [self._generate_starting_rhythm()]
        for _ in range(1, length):
            rhythm_sequence.append(
                self._generate_next_rhythm(rhythm_sequence[-1]))
        return rhythm_sequence

    def _generate_starting_rhythm(self):
        initial_index = np.random.choice(
            list(self._rhythm_indexes.values()), p=self.initial_probabilities
        )
        return self.rhythms[initial_index]

    def _generate_next_rhythm(self, current_rhythm):
        if self._does_rhythm_have_subsequent(current_rhythm):
            index = np.random.choice(
                list(self._rhythm_indexes.values()),
                p=self.transition_matrix[self._rhythm_indexes[current_rhythm]],
            )
            return self.rhythms[index]
        return self._generate_starting_rhythm()

    def _does_rhythm_have_subsequent(self, rhythm):
        return self.transition_matrix[self._rhythm_indexes[rhythm]].sum() > 0


def visualize_rhythm(rhythm_sequence):
    score = stream.Score()
    score.metadata = metadata.Metadata(title="Markov Chain Rhythm")
    part = stream.Part()
    for duration in rhythm_sequence:
        part.append(note.Note(quarterLength=duration))
    score.append(part)
    score.show()


def main():
    rhythms = [
        8,  # Dos Redondas
        7,  # Redonda + blanca con punto
        6,  # Redonda con punto
        5,  # Redonda + negra
        4,  # Redonda
        3,  # Blanca con punto
        2,  # Blanca
        1  # Negra
    ]

    initial_probabilities = [
        0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1
    ]

    # Asegúrate de que las probabilidades iniciales sumen 1
    initial_prob_sum = sum(initial_probabilities)
    if initial_prob_sum != 1:
        initial_probabilities = [
            p / initial_prob_sum for p in initial_probabilities]

    transition_matrix = [
        [0.5, 0, 0.4, 0, 0, 0.1, 0, 0],  # Dos Redondas
        [0, 0, 0.5, 0, 0.4, 0, 0.1, 0],  # Redonda + blanca con punto
        [0, 0.5, 0, 0.4, 0.1, 0, 0, 0],  # Redonda con punto
        [0.1, 0, 0, 0, 0.5, 0, 0.4, 0],  # Redonda + negra
        [0, 0, 0.5, 0.1, 0, 0.4, 0, 0],  # Redonda
        [0, 0, 0, 0, 0.5, 0, 0.1, 0.4],  # Blanca con punto
        [0, 0, 0.4, 0, 0.1, 0, 0.5, 0],  # Blanca
        [0, 0.1, 0.4, 0, 0, 0, 0.5, 0]]  # Negra

    # Asegúrate de que todas las filas de la matriz de transición sumen 1
    for i in range(len(transition_matrix)):
        row_sum = sum(transition_matrix[i])
        if row_sum != 1:
            transition_matrix[i] = [p / row_sum for p in transition_matrix[i]]

    model = MarkovChainRhythmGenerator(
        rhythms, initial_probabilities, transition_matrix)
    generated_rhythm = model.generate(12)
    with open('generated_rhythm.pkl', 'wb') as f:
        pickle.dump(generated_rhythm, f)
    # visualize_rhythm(generated_rhythm)


if __name__ == "__main__":
    main()
