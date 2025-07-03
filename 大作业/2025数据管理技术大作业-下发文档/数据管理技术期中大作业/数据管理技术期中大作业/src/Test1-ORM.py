from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, create_engine, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import csv
import time

id = 22370000
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{id}:{id}@119.3.248.160:3306/db_{id}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine(f"mysql+pymysql://{id}:{id}@119.3.248.160:3306/db_{id}?charset=utf8mb4")
# print(db)
Session = sessionmaker(bind=engine)
session = Session()


class Departments(db.Model):
    dept_no = db.Column(db.CHAR(4), primary_key=True)
    dept_name = db.Column(db.String(40), nullable=False, unique=True)
    dept_emps = db.relationship('Dept_emp', backref='department', lazy=True, cascade='all, delete')
    dept_managers = db.relationship('Dept_manager', backref='department', lazy=True, cascade='all, delete')

    def to_dict(self):
        return {
            'dept_no': self.dept_no,
            'dept_name': self.dept_name
        }


class Employees(db.Model):


# TODO: Finish the Employees Class to create the table

class Dept_emp(db.Model):


# TODO: Finish the Dept_emp Class to create the table

class Dept_manager(db.Model):


# TODO: Finish the Dept_manager Class to create the table

class Titles(db.Model):


# TODO: Finish the Titles Class to create the table

class Dept_manager_title(db.Model):


# TODO: Finish the Dept_manager_title Class to create the table


sql_trigger_insert = text("""___________________""")

sql_trigger_delete = text("""___________________""")


# TODO: Finish the insert and delete trigger by yourself

def read_csv_file(file_path):
    rows = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


with app.app_context():
    db.drop_all()
    db.create_all()

with engine.connect() as connect:
    connect.execute(sql_trigger_insert)
    connect.execute(sql_trigger_delete)

# department插入
reader = read_csv_file('./departments.csv')
# data = [{'dept_no': row['dept_no'], 'dept_name': row['dept_name']} for row in reader]
rows = []
for row in reader:
    department = Departments(
        dept_no=row['dept_no'],
        dept_name=row['dept_name']
    )
    rows.append(department)

session.bulk_save_objects(rows)
session.commit()

# employees插入
# TODO: insert data

# dept_emp插入
# TODO: insert data

# dept_manager插入
# TODO: insert data

# titles插入
# TODO: insert data
