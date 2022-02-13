from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

from app.models.vaccine_cards_model import VaccineCards
from app.configs.database import db


def get_vaccines():
    session: Session = db.session
    base_query = session.query(VaccineCards)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    records = base_query.paginate(page, per_page)

    return jsonify(records.items), HTTPStatus.OK


def cpf_checking(cpf) -> list:
    result = []
    if len(cpf) != 11:
        result.append("CPF deve ter 11 caracteres")

    try:
        int(cpf)
    except ValueError:
        result.append("CPF deve conter apenas números")

    return result


def data_checking(data) -> list:
    result = [True, True] #, ""]
    for v in data.values():
        if type(v) != str:
            result[0] = False
    keys_expected = ["cpf", "name", "vaccine_name", "health_unit_name"]
    keys_received  = [k for k in data.keys()]
    # não deu certo pq se houver a mais é diferente
    # result.append(set(keys_expected) == set(keys_received))
    for k in keys_expected:
        try:
            keys_received.index(k)
        except:
            result[1] = False
            # result[2] = result[2] + " " + k
    
    return result


def post_vaccines():
    data = request.get_json()
    data_check = data_checking(data)
    if (data_check[0] + data_check[1]) == 2:
        cpf_check = cpf_checking(data['cpf'])

        try:
            cpf_check[0]
        except:
            pass
        else:
            return jsonify({"error": cpf_check}), HTTPStatus.BAD_REQUEST

        #TODO lembro de uma DEMO em que não foi assim, mas não anotei
        #TODO preciso rever...
        data_treated = {
                'first_shot_date': datetime.now(),
                'second_shot_date': datetime.now()+timedelta(days = 90),
                'name': data['name'].upper(),
                'cpf':  data['cpf'],
                'vaccine_name': data['vaccine_name'].upper(),
                'health_unit_name': data['health_unit_name'].upper()
            }

        #record = VaccineCards(**data)
        record = VaccineCards(**data_treated)

        db.session.add(record)
        try:
            db.session.commit()
        except IntegrityError:
            return {"error": "CPF já cadastrado"}, HTTPStatus.CONFLICT

        return jsonify({"msg": record}), HTTPStatus.CREATED

    msg = []
    if not data_check[0]:
        msg.append("Campos devem ser string")
    if not data_check[1]:
        msg.append("Chave(s) inválida(s)")

    return jsonify({"error": msg}), HTTPStatus.BAD_REQUEST

