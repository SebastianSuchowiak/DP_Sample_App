from SampleApp.DataManagement.db import Employee, Salary, Address, User
from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    password = fields.Str()
    created_on = fields.DateTime()
    last_login = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return Employee(**data)


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


class SalarySchema(Schema):
    employee_id = fields.Integer()
    basic_salary = fields.Str()
    bonus = fields.Str()
    penalty = fields.Str()
    row_permission = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Salary(**data)


class AddressSchema(Schema):
    employee_id = fields.Integer()
    city = fields.Str()
    street = fields.Str()
    local_address = fields.Str()
    postal_code = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Address(**data)