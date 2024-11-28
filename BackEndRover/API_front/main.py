from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import SessionLocal, Acelerometro, BMP280, Ultrasonico, ADS1115

app = FastAPI()
origins = {
    "http://localhost:3000", "http://localhost:8000"
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints para el acelerómetro
class AcelerometroDTO(BaseModel):
    x: float = Field(..., gt=-100.0, lt=100.0)
    y: float = Field(..., gt=-100.0, lt=100.0)
    z: float = Field(..., gt=-100.0, lt=100.0)
    freefall_event: str
    motion_event: str

@app.post("/accelerometer", response_model=AcelerometroDTO)
async def create_acelerometro(data: AcelerometroDTO, db: Session = Depends(get_db)):
    lectura = Acelerometro(**data.dict())
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

@app.get("/accelerometer", response_model=list[AcelerometroDTO])
def get_acelerometro(db: Session = Depends(get_db)):
    return db.query(Acelerometro).all()

# Endpoints para el BMP280 (temperatura, presión, altitud)
class BMP280DTO(BaseModel):
    temperature: float
    pressure: float
    altitude: float

@app.post("/bmp280", response_model=BMP280DTO)
async def create_bmp280(data: BMP280DTO, db: Session = Depends(get_db)):
    lectura = BMP280(**data.dict())
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

@app.get("/bmp280", response_model=list[BMP280DTO])
def get_bmp280(db: Session = Depends(get_db)):
    return db.query(BMP280).all()

# Endpoints para el sensor ultrasónico
class UltrasonicoDTO(BaseModel):
    distance_cm: float

@app.post("/ultrasonic", response_model=UltrasonicoDTO)
async def create_ultrasonico(data: UltrasonicoDTO, db: Session = Depends(get_db)):
    lectura = Ultrasonico(**data.dict())
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

@app.get("/ultrasonic", response_model=list[UltrasonicoDTO])
def get_ultrasonico(db: Session = Depends(get_db)):
    return db.query(Ultrasonico).all()

# Endpoints para el sensor ADS1115 (lecturas analógicas)
class ADS1115DTO(BaseModel):
    analog_value: int
    voltage: float

@app.post("/ads1115", response_model=ADS1115DTO)
async def create_ads1115(data: ADS1115DTO, db: Session = Depends(get_db)):
    lectura = ADS1115(**data.dict())
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

@app.get("/ads1115", response_model=list[ADS1115DTO])
def get_ads1115(db: Session = Depends(get_db)):
    return db.query(ADS1115).all()
