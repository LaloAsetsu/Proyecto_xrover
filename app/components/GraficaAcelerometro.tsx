'use client';
//componente dedicado para la grafica del acelerometro 

import React, { useEffect, useState } from "react"; //importamos react
import axios from "axios";    //importamos axios
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";   //importamos recharts con todos los 

//definimos la interfaz de nuestra grafica usando los nombres exactos que tenemos en neustra base de datos
interface Accelerometer {
  id: number;
  valor_acel_x: number;
  valor_acel_y: number;
  valor_acel_z: number;
  fecha: string;
}

const GraficaAcelerometro = () => {
  //este estado sirve para almacenar los datos recibidos 
  const [data, setData] = useState<Accelerometer[]>([]);

  //solicitud inicial 
  useEffect(() => {
    async function fetchData() {
      try {
        //peticion de la api a donde se mandan los datos del acelerometro 
        const response = await axios.get("http://localhost:8000/acelerometro");
        setData(response.data);
      } catch (error) {
        console.error("Error fetching accelerometer data:", error);
      }
    }
    //lllamada a los datos 
    fetchData();
    //intervalo de dos segundos en el que se actualiza la grafica 
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (

    
    <div className="w-full h-[400px] p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-center text-lg font-semibold mb-4">Acelerómetro</h2>
  {/* w-full: el ancho del contenedor utiliza todo el espacio*/}
  {/* h-[400px]: altura del contenedor a 400 pixeles */}
  {/* p-4: añade un relleno de 4 unidades alrededor del contenedr */}
  {/* bg-white: fondo blanco*/}
  {/* rounded-lg: bordes redondos */}
  {/* shadow-md: sombreado moderado al contenedor para simular profundidad */}
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="fecha" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="valor_acel_x" stroke="#FF0000" name="Eje X" />
          <Line type="monotone" dataKey="valor_acel_y" stroke="#00FF00" name="Eje Y" />
          <Line type="monotone" dataKey="valor_acel_z" stroke="#0000FF" name="Eje Z" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GraficaAcelerometro;
