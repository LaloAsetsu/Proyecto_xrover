// src/app/page.tsx
//page se encarga de reunir todos los demas componentes, algunos de ellos dentro de otros componentes para construir la pagina completa
//React y sus variantes estan pensados especificamente para usar este enfoque modular para la ccreacion de apps modernas 
import Header from "./components/Header";
import SensorPanel from "./components/SensorPanel";
import CommandPanel from "./components/CommandPanel";
import Footer from "./components/Footer";
import GraficaSensorDistancia from "./components/GraficaSensorDistancia";
import ControlButtons from "./components/ControlButtons";

export default function Home() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto p-4 flex flex-col lg:flex-row gap-4">
        <section className="lg:w-1/2">
          <SensorPanel />
          
        </section>
        <section className="lg:w-1/2">
          <CommandPanel />
          <ControlButtons/>
          
        </section>
      </main>
      <Footer />
    </div>
  );
}
