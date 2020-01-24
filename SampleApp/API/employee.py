from flask_login import login_required

from SampleApp.DataManagement.db import Employee
from SampleApp.DataManagement.serialization import EmployeeSchema
from SampleApp.DataManagement.db import db
from flask import (
    Blueprint, request, jsonify
)
import logging


bp = Blueprint('employee', __name__, url_prefix='/employee')


@bp.route('/add_employee', methods=['POST'])
def add_employee():
    logging.debug('add_employee()\nInput JSON: {}'.format(request.json))
    new_employee = EmployeeSchema().load(request.json)
    db.session.add(new_employee)
    db.session.commit()
    return {'id': new_employee.id}


@bp.route('/employees', methods=['GET'])
@login_required
def get_employees():
    logging.debug("get_employees()")

    employees = Employee.query.all()
    serialized_employee = EmployeeSchema(many=True).dump(employees)
    return jsonify(serialized_employee)


@bp.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    logging.debug("get_employee({})".format(id))

    employee = Employee.query.filter_by(id=id).first()
    serialized_employee = EmployeeSchema().dump(employee)
    return serialized_employee
