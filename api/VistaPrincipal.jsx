import React from "react";
import VistaInteractivaPartitura from "./VistaInteractivaPartitura";
import VistaGrabacionAudio from "./VistaGrabacionAudio";
import { Card, CardContent } from "@/components/ui/card";

export default function VistaPrincipal() {
  return (
    <div className="p-6 space-y-6">
      <Card className="text-center">
        <CardContent className="pt-6">
          <img
            src="/logo_profesor_ritmo.png"
            alt="Profesor de Ritmo Logo"
            className="mx-auto w-32 h-auto mb-2"
          />
          <h1 className="text-3xl font-bold">Profesor de Ritmo</h1>
          <p className="text-muted-foreground">
            Por Josue Borges Diaz
          </p>
          <p className="text-base mt-2">
            Entorno musical autónomo: notación, audio, ritmo y creación moderna todo desde dentro.
          </p>
        </CardContent>
      </Card>

      <VistaInteractivaPartitura />
      <VistaGrabacionAudio />

      <footer className="text-center pt-6 text-muted-foreground text-sm">
        “Una IA generativa musical que enseña, escucha y crea contigo” 🎶
      </footer>
    </div>
  );
}
