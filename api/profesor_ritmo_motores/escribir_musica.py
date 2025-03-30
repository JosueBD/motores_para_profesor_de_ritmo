from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from music21 import stream, note, meter, clef, key
import tempfile
import uuid
import os
from pydub import AudioSegment
from midi2audio import FluidSynth

app = FastAPI()

@app.get("/escribir_musica")
def escribir_musica(
    texto: str = Query(..., description="Secuencia de notas, por ejemplo: C4 D4 E4 F4 G4 A4 B4 C5"),
    compas: str = Query("4/4"),
    clave: str = Query("G"),
    formato: str = Query("png", description="Formato de salida: png, pdf, midi, wav")
):
    part = stream.Part()
    if clave.upper() == "G":
        part.append(clef.TrebleClef())
    elif clave.upper() == "F":
        part.append(clef.BassClef())
    else:
        part.append(clef.TrebleClef())

    part.append(meter.TimeSignature(compas))
    part.append(key.KeySignature(0))

    notas = texto.strip().split()
    for i, pitch in enumerate(notas):
        m = stream.Measure(number=i+1)
        m.append(note.Note(pitch, quarterLength=1))
        part.append(m)

    score = stream.Score()
    score.insert(0, part)

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_id = uuid.uuid4().hex

        if formato == "png":
            output_path = os.path.join(tmpdirname, f"partitura_{file_id}.png")
            score.write('lily.png', fp=output_path)
            return FileResponse(output_path, media_type="image/png", filename="partitura.png")

        elif formato == "pdf":
            output_path = os.path.join(tmpdirname, f"partitura_{file_id}.pdf")
            score.write('lily.pdf', fp=output_path)
            return FileResponse(output_path, media_type="application/pdf", filename="partitura.pdf")

        elif formato == "midi":
            output_path = os.path.join(tmpdirname, f"partitura_{file_id}.mid")
            score.write('midi', fp=output_path)
            return FileResponse(output_path, media_type="audio/midi", filename="partitura.mid")

        elif formato == "wav":
            midi_path = os.path.join(tmpdirname, f"temp_{file_id}.mid")
            wav_path = os.path.join(tmpdirname, f"partitura_{file_id}.wav")
            score.write('midi', fp=midi_path)
            fs = FluidSynth()
            fs.midi_to_audio(midi_path, wav_path)
            return FileResponse(wav_path, media_type="audio/wav", filename="partitura.wav")

        else:
            return {"error": "Formato no soportado. Usa png, pdf, midi o wav."}
