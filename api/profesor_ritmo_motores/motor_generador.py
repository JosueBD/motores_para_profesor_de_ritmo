from music21 import stream, note, meter, tempo, midi

def generar_patron_ritmico(tempo_valor=100, compas_valor="4/4", dificultad="básico", compases=4):
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=tempo_valor))
    s.append(meter.TimeSignature(compas_valor))

    negra = note.Note("C4", quarterLength=1)
    negra.storedInstrument = None

    patron = {
        "básico": [1, 0, 1, 0],
        "intermedio": [1, 1, 0, 1],
        "avanzado": [1, 0.5, 0.5, 1]
    }[dificultad]

    for _ in range(compases):
        for duracion in patron:
            if duracion == 0:
                s.append(note.Rest(quarterLength=1))
            else:
                s.append(note.Note("C4", quarterLength=duracion))
    return s
