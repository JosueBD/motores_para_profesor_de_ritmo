from music21 import converter
import librosa

def analizar_midi(path):
    try:
        score = converter.parse(path)
        duraciones = [n.quarterLength for n in score.flat.notesAndRests]
        total_duracion = sum(duraciones)
        num_notas = len(score.flat.notes)
        return {
            "total_duracion": total_duracion,
            "num_notas": num_notas
        }
    except Exception as e:
        return {"error": str(e)}

def analizar_wav(path):
    try:
        y, sr = librosa.load(path)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        tempo = librosa.beat.tempo(y=y, sr=sr)
        return {
            "tempo_estimado": float(tempo[0]),
            "cantidad_golpes": len(onset_frames)
        }
    except Exception as e:
        return {"error": str(e)}
