# 📘 Resumen General – Estado Actual del Proyecto "Profesor de Ritmo"

**Responsable**: Josué Borges Díaz  
**Última actualización**: Abril 2025  
**Correo**: josuepjnv@gmail.com

---

## 🎯 Objetivo del Proyecto

Crear una **IA generativa musical autónoma**, embebida en GPT, que permita educar, crear y analizar música rítmica sin que el usuario tenga que salir del entorno de conversación. Todo debe ser accesible, interactivo y profesional.

---

## ⚙️ Motores actualmente integrados

- `escribir_musica`: Genera partitura a partir de texto musical. Exporta en PNG, PDF, MIDI, WAV.
- `generar_ritmo`: Crea patrones rítmicos según tempo, compás, dificultad.
- `analizar_midi`: Analiza compases y notas dentro de archivos MIDI.
- `analizar_wav`: Detecta tempo, beats y características rítmicas del audio.
- `comparar_ritmos`: Evalúa similitud entre un ritmo objetivo y uno interpretado por el usuario.

---

## 🧠 Tecnologías y librerías usadas

- `music21`: Partituras, análisis, exportación.
- `mido`: Generación y edición MIDI.
- `pydub` + `fluidsynth`: Sintetizador WAV desde MIDI.
- `librosa`, `scipy`: Análisis rítmico de audio.
- `FastAPI`: Backend de los motores (ya desplegado en Render).
- `OpenAPI`: Integración en GPT vía archivo `.json`.

---

## 🔗 Enlace a la IA Generativa Profesor de Ritmo

[👉 https://chatgpt.com/g/g-67dddf884b6c81919d9460325c0221c5-profesor-de-ritmo](https://chatgpt.com/g/g-67dddf884b6c81919d9460325c0221c5-profesor-de-ritmo)

---

## 🖥️ Interfaz visual integrada

La IA ya tiene:

- Menú interactivo React tipo MuseScore para ver partituras generadas.
- Selección de clave, compás, colores y nombres.
- Exportación inmediata de cualquier resultado.

---

## 🛠️ En desarrollo / por afinar

- Editor tipo staff interactivo (escritura libre desde canvas o entorno nativo)
- Soporte total a MusicXML y lectura personalizada.
- Integración con Flat.io (opcional futuro).

---

## 🧾 Documentación relacionada

- Carta enviada a OpenAI solicitando funciones de escritura musical interactiva.
- Política de privacidad subida para permitir acciones públicas.

---

## 🔐 Seguridad y acceso

Todos los motores están embebidos y protegidos. No hay almacenamiento de datos personales.

---

**Creado por**: Josué Borges Díaz  
**Licencia**: Uso educativo, sin fines comerciales  
**Contacto**: josuepjnv@gmail.com
