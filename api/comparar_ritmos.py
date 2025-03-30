from fastapi import APIRouter, File, UploadFile
from music21 import converter
import tempfile

router = APIRouter()

@router.post("/comparar_ritmos")
async def comparar_ritmos(
    file_objetivo: UploadFile = File(...),
    file_usuario: UploadFile = File(...)
):
    def extraer_pulsos(path):
        score = converter.parse(path)
        return [n.offset for n in score.flat.notes]

    try:
        # Guardar archivos
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
