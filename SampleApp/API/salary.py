from SampleApp.DataManagement.db import Salary
from SampleApp.DataManagement.serialization import SalarySchema
from SampleApp.DataManagement.db import db
from flask import (
    Blueprint, request, jsonify, Response
)
import logging
import json


bp = Blueprint('salary', __name__, url_prefix='/salary')


@bp.route('/add_salary', methods=['POST'])
def add_salary():
    logging.debug('add_salary()\nInput JSON: {}'.format(request.json))

    new_salary = SalarySchema().load(request.json)
    db.session.add(new_salary)

    try:
        db.session.commit()
    except Exception:
        msg = json.dumps({'message': 'Employee with id {} already has a salary assigned'.format(new_salary.employee_id)})
        logging.error(msg)
        return Response(
            response=msg,
            status=409,
            mimetype='application/json'
        )

    return {'id': new_salary.employee_id}


@bp.route('/salaries', methods=['GET'])
def get_salaries():
    logging.debug('get_salaries()')

    salaries = Salary.query.all()
    serialized_employee = SalarySchema(many=True).dump(salaries)
    return jsonify(serialized_employee)


@bp.route('/salary/<int:id>', methods=['GET'])
def get_salary(id):
    logging.debug('get_salary({})'.format(id))

    salary = Salary.query.filter_by(employee_id=id).first()
    print(salary)
    serialized_salary = SalarySchema().dump(salary)
    return serialized_salary
