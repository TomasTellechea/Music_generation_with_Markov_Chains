import numpy as np
from music21 import *
import pickle


class MarkovChainMelodyGenerator:
    def __init__(self, states, initial_probabilities, transition_matrix):
        self.states = states
        self.initial_probabilities = np.array(initial_probabilities)
        self.transition_matrix = np.array(transition_matrix)
        self._state_indexes = {state: i for i, state in enumerate(states)}

    def generate(self, length):
        melody = [self._generate_starting_state()]
        for _ in range(1, length):
            melody.append(self._generate_next_state(melody[-1]))
        return melody

    def _generate_starting_state(self):
        initial_index = np.random.choice(
            list(self._state_indexes.values()), p=self.initial_probabilities
        )
        return self.states[initial_index]

    def _generate_next_state(self, current_state):
        if self._does_state_have_subsequent(current_state):
            index = np.random.choice(
                list(self._state_indexes.values()),
                p=self.transition_matrix[self._state_indexes[current_state]],
            )
            return self.states[index]
        return self._generate_starting_state()

    def _does_state_have_subsequent(self, state):
        return self.transition_matrix[self._state_indexes[state]].sum() > 0


def create_training_data():
    return [
        note.Note("C4", quarterLength=1),
        note.Note("C#4", quarterLength=1),
        note.Note("G4", quarterLength=1),
        note.Note("D4", quarterLength=1),
        note.Note("D#4", quarterLength=1),
        note.Note("C#4", quarterLength=1),
        note.Note("E4", quarterLength=1),
        note.Note("F4", quarterLength=1),
        note.Note("F#4", quarterLength=1),
        note.Note("G4", quarterLength=1),
        note.Note("C#4", quarterLength=1),
        note.Note("G#4", quarterLength=1),
        note.Note("A4", quarterLength=1),
        note.Note("G4", quarterLength=1),
        note.Note("A#4", quarterLength=1),
        note.Note("B4", quarterLength=1),
    ]


def visualize_melody(melody):
    print(melody)
    score = stream.Score()
    score.metadata = metadata.Metadata(title="Markov Chain Melody")
    part = stream.Part()
    for n, d in melody:
        part.append(note.Note(n, quarterLength=d))
    score.append(part)
    score.show()


def main():
    # training_data = create_training_data()

    states = [
        ("C4", 1),
        ("C#4", 1),
        ("D4", 1),
        ("D#4", 1),
        ("E4", 1),
        ("F4", 1),
        ("F#4", 1),
        ("G4", 1),
        ("G#4", 1),
        ("A4", 1),
        ("A#4", 1),
        ("B4", 1),
    ]

    initial_probabilities = [
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0
    ]

    # Asegúrate de que las probabilidades iniciales sumen 1
    initial_prob_sum = sum(initial_probabilities)
    if initial_prob_sum != 1:
        initial_probabilities = [
            p / initial_prob_sum for p in initial_probabilities]

    transition_matrix = [
        [0, 0, 0.2, 0, 0, 0, 0, 0.6, 0.2, 0, 0, 0],
        [0, 0.2, 0, 0.2, 0, 0, 0, 0, 0.6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0.2, 0.2, 0, 0.6, 0, 0],
        [0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0.2, 0.6, 0],
        [0, 0, 0, 0.2, 0.2, 0, 0, 0, 0.6, 0, 0, 0],
        [0, 0, 0, 0.6, 0, 0, 0, 0, 0.2, 0, 0, 0.2],
        [0, 0, 0, 0, 0, 0.6, 0, 0, 0.2, 0, 0.2, 0],
        [0, 0, 0, 0.2, 0.2, 0, 0.6, 0, 0, 0, 0, 0],
        [0.2, 0, 0, 0, 0, 0, 0, 0.6, 0, 0.2, 0, 0],
        [0, 0, 0.2, 0, 0, 0, 0.2, 0, 0, 0, 0, 0.6],
        [0, 0.6, 0, 0, 0, 0, 0, 0.2, 0, 0, 0.2, 0],
        [0, 0, 0, 0.2, 0, 0, 0, 0.6, 0, 0, 0.2, 0]]

    for i in range(len(transition_matrix)):
        row_sum = sum(transition_matrix[i])
        if row_sum != 1:
            transition_matrix[i] = [p / row_sum for p in transition_matrix[i]]

    model = MarkovChainMelodyGenerator(
        states, initial_probabilities, transition_matrix)
    generated_melody = model.generate(40)

    with open('generated_melody.pkl', 'wb') as f:
        pickle.dump(generated_melody, f)
    # visualize_melody(generated_melody)


# En tu archivo principal donde generas la melodía
if __name__ == "__main__":
    main()
