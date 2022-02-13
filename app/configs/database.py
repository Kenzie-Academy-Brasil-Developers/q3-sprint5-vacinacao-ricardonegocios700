from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv

db = SQLAlchemy()

def init_app(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    
    app.db = db

    from app.models.vaccine_cards_model import VaccineCards

    