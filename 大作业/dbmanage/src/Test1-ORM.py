from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, create_engine, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import csv
import time

id = 22375080
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://db_{id}:db_{id}@rm-2zemok857yc034840vo.mysql.rds.aliyuncs.com/db_{id}?charset=utf8mb4"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:[]@localhost:3306/dbmanage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine(f"mysql+pymysql://db_{id}:db_{id}@rm-2zemok857yc034840vo.mysql.rds.aliyuncs.com/db_{id}?charset=utf8mb4")
# engine = create_engine('mysql+pymysql://root:[]@localhost:3306/dbmanage')
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
    emp_no = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(14), nullable=False, index=True) # B+Tree类型索引
    last_name = db.Column(db.String(16), nullable=False) 
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    
    dept_emps = db.relationship('Dept_emp', backref='employee', lazy=True, cascade='all, delete')
    dept_managers = db.relationship('Dept_manager', backref='employee', lazy=True, cascade='all, delete')
    titles = db.relationship('Titles', backref='employee', lazy=True, cascade='all, delete')
    
    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'birth_date': self.birth_date.strftime('%Y-%m-%d'),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'hire_date': self.hire_date.strftime('%Y-%m-%d')
        }


class Dept_emp(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    dept_no = db.Column(db.CHAR(4), db.ForeignKey('departments.dept_no', ondelete='CASCADE'), primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'dept_no': self.dept_no,
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': self.to_date.strftime('%Y-%m-%d')
        }


class Dept_manager(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    dept_no = db.Column(db.CHAR(4), db.ForeignKey('departments.dept_no', ondelete='CASCADE'), primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'dept_no': self.dept_no,
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': self.to_date.strftime('%Y-%m-%d')
        }


class Titles(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    title = db.Column(db.String(50), primary_key=True)
    from_date = db.Column(db.Date, primary_key=True)
    to_date = db.Column(db.Date, nullable=True)
    
    def to_dict(self):
        to_date_str = self.to_date.strftime('%Y-%m-%d') if self.to_date else None
        return {
            'emp_no': self.emp_no,
            'title': self.title,
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': to_date_str
        }


class Dept_manager_title(db.Model):
    emp_no = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=True)
    
    def to_dict(self):
        to_date_str = self.to_date.strftime('%Y-%m-%d') if self.to_date else None
        return {
            'emp_no': self.emp_no,
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': to_date_str
        }


sql_trigger_insert = text("""
        CREATE TRIGGER dept_manager_insert_trigger
        AFTER INSERT ON dept_manager
        FOR EACH ROW
        BEGIN
            INSERT INTO dept_manager_title (emp_no, from_date, to_date)
            VALUES (NEW.emp_no, NEW.from_date, NEW.to_date);
        END
""")

sql_trigger_delete = text("""
        CREATE TRIGGER dept_manager_delete_trigger
        AFTER DELETE ON dept_manager
        FOR EACH ROW
        BEGIN
            DELETE FROM dept_manager_title
            WHERE emp_no = OLD.emp_no;
        END
""")


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
reader = read_csv_file('./employees.csv')
rows = []
for row in reader:
    employee = Employees(
        emp_no=row['emp_no'],
        birth_date=datetime.strptime(row['birth_date'], '%Y-%m-%d').date(),
        first_name=row['first_name'],
        last_name=row['last_name'],
        gender=row['gender'],
        hire_date=datetime.strptime(row['hire_date'], '%Y-%m-%d').date()
    )
    rows.append(employee)

session.bulk_save_objects(rows)
session.commit()

# dept_emp插入
reader = read_csv_file('./dept_emp.csv')
rows = []
for row in reader:
    dept_emp = Dept_emp(
        emp_no=row['emp_no'],
        dept_no=row['dept_no'],
        from_date=datetime.strptime(row['from_date'], '%Y-%m-%d').date(),
        to_date=datetime.strptime(row['to_date'], '%Y-%m-%d').date()
    )
    rows.append(dept_emp)

session.bulk_save_objects(rows)
session.commit()

# dept_manager插入
reader = read_csv_file('./dept_manager.csv')
rows = []
for row in reader:
    dept_manager = Dept_manager(
        emp_no=row['emp_no'],
        dept_no=row['dept_no'],
        from_date=datetime.strptime(row['from_date'], '%Y-%m-%d').date(),
        to_date=datetime.strptime(row['to_date'], '%Y-%m-%d').date()
    )
    rows.append(dept_manager)

session.bulk_save_objects(rows)
session.commit()

# titles插入
reader = read_csv_file('./titles.csv')
rows = []
for row in reader:
    title = Titles(
        emp_no=row['emp_no'],
        title=row['title'],
        from_date=datetime.strptime(row['from_date'], '%Y-%m-%d').date(),
        to_date=datetime.strptime(row['to_date'], '%Y-%m-%d').date() if row['to_date'] else None
    )
    rows.append(title)

session.bulk_save_objects(rows)
session.commit()
