// src/app/components/SensorPanel.tsx
//componente donde reunimos toadas nuetras graficas para presentarlas en la parte izquierda de nuestra pagina web
//importamos todas nuestras graficas 
import React from "react";
import GraficaSensorDistancia from "./GraficaSensorDistancia";
import GraficaAcelerometro from "./GraficaAcelerometro";
import GraficaBME from "./GraficaBME"; 
import GraficaSensor4 from "./GraficaSensor4"; 

export default function SensorPanel() {
  return (
    <div className="bg-white p-6 shadow-lg rounded-lg mb-6">
      {/* bg-white: fondo blanco */}
      {/* p-6: relleno de 6 unidades al rededor del contenedor  */}
      {/* shadow-lg: sombra grande */}
      {/* rounded-lg: bordes redondeados bien grandes*/}
      {/* mb-6:  margen inferior de 6 unidades */}
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
