import json

from flask_login import login_required

from SampleApp.DataManagement.db import Address
from SampleApp.DataManagement.serialization import AddressSchema
from SampleApp.DataManagement.db import db
from flask import (
    Blueprint, request, jsonify,
    Response)
import logging


bp = Blueprint('address', __name__, url_prefix='/address')


@bp.route('/add_address', methods=['POST'])
@login_required
def add_address():
    logging.debug('add_address()\nInput JSON: {}'.format(request.json))

    new_address = AddressSchema().load(request.json)
    db.session.add(new_address)

    try:
        db.session.commit()
    except Exception:
        msg = json.dumps({'message': 'Employee with id {} already has a salary assigned'.format(new_address.employee_id)})
        logging.error(msg)
        return Response(
            response=msg,
            status=409,
            mimetype='application/json'
        )


    db.session.commit()
    return {'id': new_address.employee_id}


@bp.route('/addresses', methods=['GET'])
@login_required
def get_addresses():
    logging.debug("get_addresses()")

    addresses = Address.query.all()
    serialized_address = AddressSchema(many=True).dump(addresses)
    return jsonify(serialized_address)


@bp.route('/address/<int:id>', methods=['GET'])
@login_required
def get_address(id):
    logging.debug('get_address({})'.format(id))

    address = Address.query.filter_by(employee_id=id).first()
    serialized_address = AddressSchema().dump(address)
    return serialized_address
