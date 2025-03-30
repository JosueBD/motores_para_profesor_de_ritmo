from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from music21 import stream, note, meter, clef, tempo, key
import tempfile
import uuid
import os
import random

router = APIRouter()

@router.get("/generar_ritmo")
def generar_ritmo(
    tempo_val: int = Query(..., description="Tempo en BPM"),
    compas: str = Query(..., description="Compás, por ejemplo: 4/4"),
    dificultad: str = Query(..., description="básico, intermedio o avanzado"),
    compases: int = Query(..., description="Cantidad de compases")
):
    # Configurar partitura
    part = stream.Part()
    part.append(clef.PercussionClef())
    part.append(tempo.MetronomeMark(number=tempo_val))
    part.append(meter.TimeSignature(compas))
    part.append(key.KeySignature(0))  # No tonalidad

    # Notas base (percusión)
    duraciones = [0.25, 0.5, 1.0]
    dificultad_map = {
        "básico": [1.0],
        "intermedio": [0.5, 1.0],
        "avanzado": [0.25, 0.5, 1.0]
    }
    posibles_duraciones = dificultad_map.get(dificultad, [1.0])

    for i in range(compases):
        m = stream.Measure(number=i + 1)
        duracion_restante = meter.TimeSignature(compas).barDuration.quarterLength
        while duracion_restante > 0:
            dur = random.choice(posibles_duraciones)
            if dur <= duracion_restante:
                perc_note = note.Unpitched()
                perc_note.duration.quarterLength = dur
                perc_note.stemDirection = "up"
                m.append(perc_note)
                duracion_restante -= dur
        part.append(m)

    score = stream.Score()
    score.append(part)

    with tempfile.TemporaryDirectory() as tmpdir:
        file_id = uuid.uuid4().hex
        output_path = os.path.join(tmpdir, f"ritmo_{file_id}.mid")
        score.write('midi', fp=output_path)
        return FileResponse(output_path, media_type="audio/midi", filename="ritmo_generado.mid")
