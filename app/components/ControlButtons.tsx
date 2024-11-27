'use client';

import React from 'react';

const ControlButtons: React.FC = () => {
  const sendCommand = async (command: string): Promise<void> => {
    try {
      const response = await fetch('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
      });

      const result = await response.json();
      console.log(result.message);
    } catch (error) {
      console.error('Error al enviar el comando:', error);
    }
  };

  return (
    <div className="control-panel sticky top-4 bg-white p-4 rounded shadow-md">
      <div className="flex flex-col items-center">
        {/* Fila de botones WASD */}
        <div className="flex gap-2">
          <button
            onClick={() => sendCommand('w')}
            className="bg-green-500 text-white p-8 rounded-lg w-24"
          >
            W
          </button>
        </div>

        <div className="flex gap-2 my-2">
          <button
            onClick={() => sendCommand('a')}
            className="bg-yellow-500 text-white p-8 rounded-lg w-24"
          >
            A
          </button>
          <button
            onClick={() => sendCommand('s')}
            className="bg-green-500 text-white p-8 rounded-lg w-24"
          >
            S
          </button>
          <button
            onClick={() => sendCommand('d')}
            className="bg-yellow-500 text-white p-8 rounded-lg w-24"
          >
            D
          </button>
        </div>

        {/* Botón de Parar debajo */}
        <div className="mt-4">
          <button
            onClick={() => sendCommand('stop')}
            className="bg-red-500 text-white p-8 rounded-lg w-24"
          >
            Parar
          </button>
        </div>
      </div>
    </div>
  );
};

export default ControlButtons;
