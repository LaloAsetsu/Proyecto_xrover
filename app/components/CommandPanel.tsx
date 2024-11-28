import React from "react";
// src/app/components/CommandPanel.tsx
export default function CommandPanel() {
    return (
    //este seria el panel de comandos, por falta de tiempo no fue implementado completamente pero a continuacion
    //explicare que hacen los estilos en typewind

//el contenedor principal tiene fondo blanco, padding de 6 unidades, sombra, y bordes redondeados
      <div className="bg-white p-6 shadow-lg rounded-lg">
        <div className="mb-6">
        {/*titulo con tamaño de texto grande, negrita y margen inferior de 2 unidades */}
          <h2 className="text-2xl font-semibold mb-2">Instrucciones por Ejecutarse</h2>
          <p>Mover adelante, Girar a la derecha</p>
        </div>
        <div className="mb-6">
          <textarea
         {/*el area de texto con estilo de ancho completo, padding, borde redondeado */}
            className="w-full p-2 border rounded-lg"
            placeholder="Ingrese comandos aquí..."
          ></textarea>
     {/*clase boton encargada de mandar comandos escritos, con un fondo azul, texto blanco y bordes redondeados */}
          <button className="bg-blue-500 text-white p-2 rounded-lg mt-2 w-full">Ejecutar</button>
        </div>
        {/*contenedor flexible, para elemntos flexibles con un espacio pequeno entre ellos */}
        <div className="flex flex-wrap gap-2">
        </div>
      </div>
    );
  }
  
