'use client';

import React from 'react';
//estos son lso botones con los que se podria enviar los comandos para el movimiento de carrito
//envirian w,a,s y d 

const ControlButtons: React.FC = () => {
  const sendCommand = async (command: string): Promise<void> => {
    try {
      const response = await fetch('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
      });

      const result = await response.json();
      console.log(result.message);   //mensaje de respuesta
    } catch (error) {             //manejo de erroes
      console.error('Error al enviar el comando:', error);
    }
  };

  return (
  //el ontenedor principal del panel de control, con fondo blanco, bordes redondeados y efecto de sombreado
    <div className="control-panel sticky top-4 bg-white p-4 rounded shadow-md">
      <div className="flex flex-col items-center">
        {/*botones  WASD */}
        <div className="flex gap-2">
   {/*el boton de W y S tienen un fondo verde, texto blanco y bordes redondeados */}
          <button
            onClick={() => sendCommand('w')}
            className="bg-green-500 text-white p-8 rounded-lg w-24"
          >
            W
          </button>
        </div>

        <div className="flex gap-2 my-2">
  {/* los botones A y D teinen fondo amarillo, texto blanco y bordes redondeados */}
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

        {/*boton de PARAR debajo de los botones de control */}
        <div className="mt-4">
   {/* por convencion el color rojo se asocia con errores o urgencia, asi que nuestro boton PARAR tiene este color */}
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
