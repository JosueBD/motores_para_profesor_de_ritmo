import React, { useState } from "react";
import { Button } from "@/components/ui/button";

export default function VistaGrabacionAudio() {
  const [grabando, setGrabando] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [chunks, setChunks] = useState([]);

  const iniciarGrabacion = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const tempChunks = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) tempChunks.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(tempChunks, { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        setAudioURL(url);
        setChunks([]);
      };

      recorder.start();
      setMediaRecorder(recorder);
      setChunks(tempChunks);
      setGrabando(true);
    } catch (err) {
      console.error("Error al acceder al micrófono:", err);
    }
  };

  const detenerGrabacion = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setGrabando(false);
    }
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-2xl font-bold">🎙️ Grabador de Audio</h2>
      <div className="space-x-2">
        <Button onClick={iniciarGrabacion} disabled={grabando}>🎤 Iniciar grabación</Button>
        <Button onClick={detenerGrabacion} disabled={!grabando}>🛑 Detener</Button>
      </div>
      {audioURL && (
        <div className="pt-4">
          <h3 className="text-lg font-semibold">▶️ Reproducción:</h3>
          <audio controls src={audioURL}></audio>
        </div>
      )}
    </div>
  );
}
