# Profesor de Ritmo – Motores musicales para IA generativa

**Profesor de Ritmo** es un entorno musical autónomo diseñado para educar, generar y analizar ritmo moderno desde una IA generativa, sin que el usuario tenga que salir del entorno. Este repositorio contiene los **motores musicales internos** que permiten a la IA operar con notación, audio, MIDI, visualización y exportación.

---

## 🌍 Tecnologías y librerías integradas

- **FastAPI** – Framework principal de los motores
- **music21** – Análisis y generación de partituras
- **mido** – Manejo y exportación de archivos MIDI
- **pydub** + **fluidsynth** – Sintetizador de audio WAV desde MIDI
- **librosa** + **scipy** – Análisis de audio (WAV)
- **matplotlib** – Visualizaciones rítmicas (en futuras versiones)
- **uuid**, **tempfile** – Control de archivos temporales para exportación

---

## ⚙️ Funciones del motor

Cada función está disponible como un **endpoint de la API**, integrado en la IA generativa:

### `/escribir_musica`
Genera una partitura a partir de texto musical (notas y compás) y exporta en formato:
- PNG (imagen de la partitura)
- PDF (documento imprimible)
- MIDI (archivo ejecutable)
- WAV (archivo de audio generado desde MIDI)

### `/generar_ritmo`, `/analizar_midi`, `/analizar_wav`, `/comparar_ritmos`
Motores internos para:
- Crear ritmos según tempo, compás y dificultad
- Analizar archivos MIDI o WAV cargados por el usuario
- Comparar ritmos y detectar errores entre dos ejecuciones

---

## 🔗 Integración con el GPT "Profesor de Ritmo"

Estos motores están expuestos mediante una especificación **OpenAPI (.json)** que fue cargada en ChatGPT mediante acciones personalizadas.

La IA generativa:
- Llama directamente a estos motores
- Exporta resultados en tiempo real
- Provee partituras, audio y análisis automáticos
- Ofrece retroalimentación en lenguaje pedagógico

---

## 🎧 Interoperabilidad con programas profesionales

Los archivos generados por el sistema pueden abrirse o importarse en:

| Programa     | Formatos compatibles     |
|--------------|--------------------------|
| MuseScore    | PDF, MIDI, MusicXML      |
| Sibelius     | MIDI, MusicXML           |
| Finale       | MIDI, MusicXML           |
| Dorico       | MIDI, MusicXML           |

---

## 🚀 Futuras expansiones

- Integración con **Flat.io** para edición colaborativa
- Exportación nativa a **MusicXML**
- Acceso a modelos de generación rítmica de **Magenta (Google)**
- Editor web de patrones rítmicos
- Motor de retroalimentación para lectura a primera vista

---

## 📍 Crédito y licencia

**Creado por:** Josué Borges Díaz  
**Proyecto:** IA generativa pedagógica  
**Licencia:** Abierto para uso educativo y no comercial. Para colaboraciones o integraciones, contactar al autor.

---

Para usar la IA generativa Profesor de Ritmo, entra en:  
👉 [https://chatgpt.com/g/g-67dddf884b6c81919d9460325c0221c5-profesor-de-ritmo](https://chatgpt.com/g/g-67dddf884b6c81919d9460325c0221c5-profesor-de-ritmo)
