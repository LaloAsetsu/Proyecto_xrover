// src/app/components/SensorPanel.tsx
import React from "react";
import GraficaSensorDistancia from "./GraficaSensorDistancia";
import GraficaAcelerometro from "./GraficaAcelerometro";
import GraficaBME from "./GraficaBME"; // Asegúrate de que el archivo tenga el nombre correcto.
import GraficaSensor4 from "./GraficaSensor4"; // Asegúrate de que este archivo también coincida.

export default function SensorPanel() {
  return (
    <div className="bg-white p-6 shadow-lg rounded-lg mb-6">
      <h2 className="text-2xl font-semibold mb-2">Sensor Distancia</h2>
      <hr className="my-4" />
      <GraficaSensorDistancia />

      <h2 className="text-2xl font-semibold mb-2">Acelerómetro</h2>
      <hr className="my-4" />
      <GraficaAcelerometro />

      <h2 className="text-2xl font-semibold mb-2">BME Sensor</h2>
      <hr className="my-4" />
      <GraficaBME />

      <h2 className="text-2xl font-semibold mb-2">Sensor 4</h2>
      <hr className="my-4" />
      <GraficaSensor4 />
    </div>
  );
}
