

from fastapi import FastAPI, UploadFile
from .profesor_ritmo_motores import motor_generador, motor_analizador, motor_comparador

import tempfile

app = FastAPI()

@app.get("/generar_ritmo")
def generar_ritmo(tempo: int = 100, compas: str = "4/4", dificultad: str = "básico", compases: int = 4):
    s = motor_generador.generar_patron_ritmico(tempo, compas, dificultad, compases)
    midi_path = tempfile.NamedTemporaryFile(suffix=".mid", delete=False).name
    s.write("midi", fp=midi_path)
    return {"midi_path": midi_path}

@app.post("/analizar_midi")
async def analizar_midi(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
        tmp.write(await file.read())
        return motor_analizador.analizar_midi(tmp.name)

@app.post("/analizar_wav")
async def analizar_wav(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        return motor_analizador.analizar_wav(tmp.name)

@app.post("/comparar_ritmos")
async def comparar(file_objetivo: UploadFile, file_usuario: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp2:
        tmp1.write(await file_objetivo.read())
        tmp2.write(await file_usuario.read())
        return motor_comparador.comparar_ritmos(tmp1.name, tmp2.name)
