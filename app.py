from flask import Flask, jsonify, abort, request

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, post_load


DB_USER = 'server'
DB_PASSWORD = '123'
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/projekt_test'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    position = db.Column(db.String(100))
    row_permission = db.Column(db.String(100))

    address = db.relationship("Address", uselist=False, back_populates="employee")
    salary = db.relationship("Salary", uselist=False, back_populates="employee")


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    position = fields.Str()
    row_permission = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Employee(**data)


class Salary(db.Model):
    __tablename__  = 'salary'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    basic_salary = db.Column(db.Float)
    bonus = db.Column(db.Float)
    penalty = db.Column(db.Float)
    row_permission = db.Column(db.String(100))

    employee = db.relationship("Employee", uselist=False, back_populates="salary")


class Address(db.Model):
    __tablename__ = 'address'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    city = db.Column(db.String)
    street = db.Column(db.String)
    local_address = db.Column(db.String)
    postal_code = db.Column(db.String)

    employee = db.relationship("Employee", uselist=False, back_populates="address")


db.create_all()
db.session.commit()


@app.route('/add_employee', methods=['POST'])
def add_employee():
    new_employee = EmployeeSchema().load(request.json)
    db.session.add(new_employee)
    db.session.commit()
    return {'id': new_employee.id}


@app.route('/employees', methods=['GET'])
def get_employees():
    employee = Employee.query.all()
    serialized_employee = EmployeeSchema(many=True).dump(employee)
    return jsonify(serialized_employee)


@app.route('/employee/<int:id>', methods=['GET'])
def get_role(id):
    employee = Employee.query.filter_by(id=id).first()
    print(employee)
    serialized_employee = EmployeeSchema().dump(employee)
    return serialized_employee


@app.route('/', methods=['GET'])
def make_user():
    return "Hello!"


if __name__ == '__main__':
    app.run(debug=True)

