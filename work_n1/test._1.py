import pickle
from music21 import *

# Cargar la melodía desde el archivo pickle
with open('generated_melody.pkl', 'rb') as f:
    generated_melody = pickle.load(f)


# cargamos el ritmo
with open('generated_rhythm.pkl', 'rb') as f:
    generated_rhythm = pickle.load(f)

score = stream.Score()
score.metadata = metadata.Metadata(title="Markov Chain melody")
part = stream.Part()


# Cargar la melodía desde el archivo pickle
with open('generated_melody.pkl', 'rb') as f:
    generated_melody = pickle.load(f)

# Cargar el ritmo desde el archivo pickle
with open('generated_rhythm.pkl', 'rb') as f:
    generated_rhythm = pickle.load(f)

score = stream.Score()
score.metadata = metadata.Metadata(title="Markov Chain melody")

# Crear una parte para la melodía y el ritmo combinados
part = stream.Part()

for i in range(len(generated_melody)):
    # Obtener nombre y duración del pitch de la melodía
    pitch_name, _ = generated_melody[i]
    duration_value = generated_rhythm[i]  # Obtener la duración del ritmo

    # Crear un objeto Note con el pitch y duración correspondientes
    new_note = note.Note(pitch_name)
    new_note.duration = duration.Duration(duration_value)

    # Agregar la nota a la parte
    part.append(new_note)

# Agregar la parte al puntaje
score.append(part)

# Mostrar el puntaje
score.show()


score.append(part)
score.show()
