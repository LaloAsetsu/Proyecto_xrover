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

interface Sensor4 {
  id: number;
  valor_res_luz: number;
  fecha: string;
}

const GraficaSensor4 = () => {
  const [data, setData] = useState<Sensor4[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("http://localhost:8000/adc");
        setData(response.data);
      } catch (error) {
        console.error("Error fetching Sensor 4 data:", error);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-[400px] p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-center text-lg font-semibold mb-4">Sensor 4</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="fecha" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey=" valor_res_luz" stroke="#8A2BE2" name="Valor Sensor" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GraficaSensor4;
