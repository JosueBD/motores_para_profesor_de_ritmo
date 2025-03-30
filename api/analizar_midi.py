from fastapi import APIRouter, File, UploadFile
from music21 import converter, meter
import tempfile

router = APIRouter()

@router.post("/analizar_midi")
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
