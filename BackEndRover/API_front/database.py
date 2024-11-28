from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Conexión a la base de datos MySQL
DATABASE_URL = "mysql+pymysql://root:Lalito24571$@localhost/proyecto_xrover"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo para la tabla del acelerómetro
class Acelerometro(Base):
    __tablename__ = "accelerometer"
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    freefall_event = Column(String(10))
    motion_event = Column(String(10))
    fecha = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla BMP280 (temperatura, presión y altitud)
class BMP280(Base):
    __tablename__ = "bmp280"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    pressure = Column(Float)
    altitude = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla del sensor ultrasónico
class Ultrasonico(Base):
    __tablename__ = "ultrasonic"
    id = Column(Integer, primary_key=True, index=True)
    distance_cm = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla del sensor ADS1115 (lectura analógica)
class ADS1115(Base):
    __tablename__ = "ads1115"
    id = Column(Integer, primary_key=True, index=True)
    analog_value = Column(Float)
    voltage = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
