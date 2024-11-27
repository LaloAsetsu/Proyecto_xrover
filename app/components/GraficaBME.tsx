'use client';

import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

interface presion {
  id: number;
  valor_temperatura: number;
  valor_presion: number;
  valor_altitud: number;
  fecha: string;
}

const GraficaBME = () => {
  const [data, setData] = useState<BME[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("http://localhost:8000/presion");
        setData(response.data);
      } catch (error) {
        console.error("Error fetching BME data:", error);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-[400px] p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-center text-lg font-semibold mb-4">Datos del BME</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="fecha" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="valor_temperatura" stroke="#FF4500" name="Temperatura" />
          <Line type="monotone" dataKey="valor_presion" stroke="#1E90FF" name="Presión" />
          <Line type="monotone" dataKey="valor_altitud" stroke="#32CD32" name="Humedad" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GraficaBME;
