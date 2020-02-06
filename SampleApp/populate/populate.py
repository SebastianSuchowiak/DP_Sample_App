from faker import Faker
from random import gauss, randint

from SampleApp.DataManagement.db import Employee, Salary, Address


def populate_employees(db, n):
    fake = Faker(['pl_PL'])

    datas = [{**create_random_employee_data(fake)} for i in range(1,n+1)]
    employees = [create_employee_from_data(data) for data in datas]
    salaries = [create_salary_from_data(data) for data in datas]
    addresses = [create_address_from_data(data) for data in datas]

    for employee, salary, address in zip(employees, salaries, addresses):
        employee.salary = salary
        employee.address =address

    db.session.add_all(employees)

    db.session.commit()



def create_random_employee_data(fake):
    name = fake.name()
    email = f'{name.split()[0]}.{name.split()[1]}@{fake.email().split("@")[1]}'.lower()
    city = fake.city()
    street = fake.street_name()
    building_number = fake.building_number()
    postal_code = fake.postcode()
    phone_number = fake.phone_number()
    salary = float(int(gauss(3500, 500)))
    position = fake.job()

    if randint(0, 1):
        penalty = 0.
        bonus = float(int(gauss(500, 150)))
    else:
        bonus = 0.
        penalty = float(int(gauss(300, 50)))

    return {
        'name': name,
        'email': email,
        'position': position,
        'city': city,
        'street': street,
        'local_address': building_number,
        'postal_code': postal_code,
        'phone': phone_number,
        'basic_salary': salary,
        'penalty': penalty,
        'bonus': bonus
    }


def create_employee_from_data(data):
    employee_data = {k: data[k] for k in data.keys() & {'name', 'phone', 'email', 'position'}}
    return Employee(**employee_data)


def create_salary_from_data(data):
    salary_data = {k: data[k] for k in data.keys() & {'basic_salary', 'penalty', 'bonus'}}
    return Salary(**salary_data)


def create_address_from_data(data):
    address_data = {k: data[k] for k in data.keys() & {'city', 'street', 'postal_code', 'local_address'}}
    return Address(**address_data)


if __name__ == '__main__':
    populate_employees('s', 5)