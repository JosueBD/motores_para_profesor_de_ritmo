from fastapi import APIRouter, File, UploadFile
import librosa
import tempfile

router = APIRouter()

@router.post("/analizar_wav")
async def analizar_wav(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        y, sr = librosa.load(tmp_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        return {
            "tempo_estimado": round(tempo),
            "beats_detectados": len(beats),
        }
    except Exception as e:
        return {"error": str(e)}
