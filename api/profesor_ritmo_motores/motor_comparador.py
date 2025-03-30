from music21 import converter

def comparar_ritmos(path1, path2):
    try:
        s1 = converter.parse(path1)
        s2 = converter.parse(path2)

        notas1 = [n.quarterLength for n in s1.flat.notesAndRests]
        notas2 = [n.quarterLength for n in s2.flat.notesAndRests]

        min_len = min(len(notas1), len(notas2))
        coincidencias = sum(1 for i in range(min_len) if notas1[i] == notas2[i])

        return {
            "coincidencias": coincidencias,
            "total_notas_comparadas": min_len,
            "porcentaje": round((coincidencias / min_len) * 100, 2)
        }
    except Exception as e:
        return {"error": str(e)}
