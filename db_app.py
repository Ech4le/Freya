from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, DateTime, Integer, BigInteger
from dotenv import dotenv_values
import sqlalchemy as db

Base = declarative_base()


class Readings(Base):
    __tablename__ = 'raw'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    ground_hum = Column(Float)
    air_hum = Column(Float)
    air_temp = Column(Float)
    lux = Column(BigInteger)
    water_temp = Column(Float)
    water_level = Column(Integer)


def init_db():
    DB_URI = dotenv_values()['DB_URI']
    engine = db.create_engine(DB_URI)
    Base.metadata.create_all(engine)

    return engine