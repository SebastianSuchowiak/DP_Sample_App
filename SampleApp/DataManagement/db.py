from itsdangerous import TimestampSigner, URLSafeSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from SampleApp import db


class User(db.Model):
    __tablename__ = 'flasklogin-users'
    extend_existing = True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    @staticmethod
    def generate_password(password):
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        signer = TimestampSigner('secret-key')
        token = signer.sign(self.username).decode('utf-8')
        serializer = URLSafeSerializer('secret-key')
        serialized_token = serializer.dumps(token)
        return serialized_token

    def __str__(self):
        return f'username: {self.username}'


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    position = db.Column(db.String(100))

    address = db.relationship("Address", uselist=False, back_populates="employee")
    salary = db.relationship("Salary", uselist=False, back_populates="employee")


class Salary(db.Model):
    __tablename__ = 'salary'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    basic_salary = db.Column(db.Float)
    bonus = db.Column(db.Float)
    penalty = db.Column(db.Float)

    employee = db.relationship("Employee", uselist=False, back_populates="salary")


class Address(db.Model):
    __tablename__ = 'address'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    city = db.Column(db.String)
    street = db.Column(db.String)
    local_address = db.Column(db.String)
    postal_code = db.Column(db.String)

    employee = db.relationship("Employee", uselist=False, back_populates="address")

