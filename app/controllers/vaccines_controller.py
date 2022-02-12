from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session

from app.models.vaccine_cards_model import VaccineCards
from app.configs.database import db


def get_vaccines():
    session: Session = db.session
    # vamos padronizar uma base_query
    base_query = session.query(VaccineCards)
    query_params = request.args

    records = base_query.filter_by(**query_params).order_by(VaccineCards.id)

    return jsonify(records.items), HTTPStatus.OK