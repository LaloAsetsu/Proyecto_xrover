from sqlalchemy import create_engine, Column, Integer, Date, Float, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#DATABASEURL = "mysql+pymysql://root:M1n3cr9f7_LJ@localhost/raspberry_1"
DATABASEURL = "mysql+pymysql://weccat:tacoverde@10.48.233.73/raspberry_2"
#               mysql+pymysql://root:Password@ip/name_database

engine = create_engine(DATABASEURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)
Base = declarative_base()


class Ultrasonico(Base):
    __tablename__ = "ultrasonico"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, index=True)
    valor_distancia_cm = Column(Float)

class Adc(Base):
    __tablename__ = "adc"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, index=True)
    valor_res_luz = Column(Float)
    voltage = Column(Float)

class Acelerometro(Base):
    __tablename__ = "acelerometro"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, index=True)
    valor_acel_x = Column(Float)
    valor_acel_y = Column(Float)
    valor_acel_z = Column(Float)


class Presion(Base):
    __tablename__ = "presion"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, index=True)
    valor_temperatura = Column(Float)
    valor_presion = Column(Float)
    valor_altitud = Column(Float)