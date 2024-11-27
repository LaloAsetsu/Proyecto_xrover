import React from "react";
// src/app/components/CommandPanel.tsx
export default function CommandPanel() {
    return (
      <div className="bg-white p-6 shadow-lg rounded-lg">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">Instrucciones por Ejecutarse</h2>
          <p>Mover adelante, Girar a la derecha</p>
        </div>
        <div className="mb-6">
          <textarea
            className="w-full p-2 border rounded-lg"
            placeholder="Ingrese comandos aquí..."
          ></textarea>
          <button className="bg-blue-500 text-white p-2 rounded-lg mt-2 w-full">Ejecutar</button>
        </div>
        <div className="flex flex-wrap gap-2">
     
        </div>
      </div>
    );
  }
  