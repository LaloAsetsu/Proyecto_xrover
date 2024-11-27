from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import SessionLocal, Ultrasonico, Acelerometro, Presion , Adc

app = FastAPI()
origins = {
    "http://localhost:8000","http://localhost:3000"
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependencia para la conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema Pydantic para validar la entrada de datos
class UltrasonicoDTO(BaseModel):
    id: int
    fecha: datetime
    valor_distancia_cm: float

    class Config:
        from_attributes = True

class AdcDTO(BaseModel):
    id: int
    fecha: datetime
    valor_res_luz: float
    voltage: float

    class Config:
        from_attributes = True

class AcelerometroDTO(BaseModel):
    id: int
    fecha: datetime
    valor_acel_x: float
    valor_acel_y: float
    valor_acel_z: float

    class Config:
        from_attributes = True

class PresionDTO(BaseModel):
    id: int
    fecha: datetime
    valor_temperatura: float
    valor_presion: float
    valor_altitud: float

    class Config:
        from_attributes = True

#class

# Obtener todos los registros
@app.get("/ultrasonico")
def get_data(db: Session = Depends(get_db)):
    data = db.query(Ultrasonico).all()
    return data

@app.get("/adc")
def get_data(db: Session = Depends(get_db)):
    data = db.query(Adc).all()
    return data

@app.get("/acelerometro")
def get_data(db: Session = Depends(get_db)):
    data = db.query(Acelerometro).all()
    return data

@app.get("/presion")
def get_data(db: Session = Depends(get_db)):
    data = db.query(Presion).all()
    return data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)