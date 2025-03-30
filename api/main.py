from fastapi import FastAPI, Query, File, UploadFile
from fastapi.responses import FileResponse
from music21 import stream, note, meter, clef, key, tempo, converter
import tempfile
import uuid
import os
import random
import librosa
from pydub import AudioSegment
from midi2audio import FluidSynth

app = FastAPI()

# ----------------------
# 🎼 /escribir_musica
# ----------------------
@app.get("/escribir_musica")
def escribir_musica(
    texto: str = Query(...),
    compas: str = Query("4/4"),
    clave: str = Query("G"),
    formato: str = Query("png")
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


# ----------------------
# 🥁 /generar_ritmo
# ----------------------
@app.get("/generar_ritmo")
def generar_ritmo(
    tempo_val: int = Query(...),
    compas: str = Query(...),
    dificultad: str = Query(...),
    compases: int = Query(...)
):
    part = stream.Part()
    part.append(clef.PercussionClef())
    part.append(tempo.MetronomeMark(number=tempo_val))
    part.append(meter.TimeSignature(compas))
    part.append(key.KeySignature(0))

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


# ----------------------
# 🎧 /analizar_midi
# ----------------------
@app.post("/analizar_midi")
async def analizar_midi(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        score = converter.parse(tmp_path)
        analysis = []

        for part in score.parts:
            for i, measure in enumerate(part.getElementsByClass("Measure")):
                notes = measure.notes
                dur_total = sum(n.duration.quarterLength for n in notes)
                analysis.append({
                    "compás": i + 1,
                    "cantidad_de_notas": len(notes),
                    "duración_total": dur_total
                })

        return {"resultado": analysis}
    except Exception as e:
        return {"error": str(e)}


# ----------------------
# 🔍 /analizar_wav
# ----------------------
@app.post("/analizar_wav")
async def analizar_wav(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        y, sr = librosa.load(tmp_path)
        tempo_val, beats = librosa.beat.beat_track(y=y, sr=sr)
        return {
            "tempo_estimado": round(tempo_val),
            "beats_detectados": len(beats)
        }
    except Exception as e:
        return {"error": str(e)}


# ----------------------
# 🧮 /comparar_ritmos
# ----------------------
@app.post("/comparar_ritmos")
async def comparar_ritmos(
    file_objetivo: UploadFile = File(...),
    file_usuario: UploadFile = File(...)
):
    def extraer_pulsos(path):
        score = converter.parse(path)
        return [n.offset for n in score.flat.notes]

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as f1:
            f1.write(await file_objetivo.read())
            path1 = f1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as f2:
            f2.write(await file_usuario.read())
            path2 = f2.name

        pulses1 = extraer_pulsos(path1)
        pulses2 = extraer_pulsos(path2)

        diferencia = abs(len(pulses1) - len(pulses2))
        coincidencias = sum(1 for p in pulses1 if p in pulses2)
        porcentaje = (coincidencias / max(len(pulses1), 1)) * 100

        return {
            "compases_comparados": min(len(pulses1), len(pulses2)),
            "coincidencias_de_pulso": coincidencias,
            "porcentaje_de_coincidencia": f"{porcentaje:.2f}%",
            "diferencia_en_total_de_pulsos": diferencia
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/comparar_ritmos")
async def comparar(file_objetivo: UploadFile, file_usuario: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp2:
        tmp1.write(await file_objetivo.read())
        tmp2.write(await file_usuario.read())
        return motor_comparador.comparar_ritmos(tmp1.name, tmp2.name)
