from flask import Blueprint
from app.controllers.vaccines_controller import get_vaccines

bp = Blueprint("vaccinations", __name__, url_prefix="/vaccinations")

bp.get("")(get_vaccines)