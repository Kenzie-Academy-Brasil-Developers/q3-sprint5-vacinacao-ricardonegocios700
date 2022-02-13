from sqlalchemy import Column, Integer, String, DateTime
from dataclasses import dataclass

from app.configs.database import db


@dataclass
class VaccineCards(db.Model):
    __tablename__ = "vaccine_cards"

    cpf: str = Column(String, primary_key=True)
    name: str = Column(String, nullable=False)
    first_shot_date: str = Column(DateTime)
    second_shot_date: str = Column(DateTime)
    vaccine_name: str = Column(String, nullable=False)
    health_unit_name: str = Column(String)

