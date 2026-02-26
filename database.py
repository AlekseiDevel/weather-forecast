import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()


class RequestLog(Base):
    __tablename__ = 'requests_log'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    city = Column(String)
    status_code = Column(Integer)

    weather_entries = relationship("WeatherData", back_populates="request")


class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests_log.id'))
    temperature = Column(Float)
    humidity = Column(Integer)
    description = Column(String)

    request = relationship("RequestLog", back_populates="weather_entries")


# Получаем URL из .env. Для теста можно заменить на 'sqlite:///./test.db'
engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///./test.db'))
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)