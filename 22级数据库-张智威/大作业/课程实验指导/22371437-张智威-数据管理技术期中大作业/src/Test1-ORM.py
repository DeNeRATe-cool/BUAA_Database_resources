from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, create_engine, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import csv
import time

id = 22371437
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{id}:{id}@119.3.248.160:3306/db_{id}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(f"mysql+pymysql://{id}:{id}@119.3.248.160:3306/db_{id}?charset=utf8mb4")
db = SQLAlchemy(app)
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
    emp_no = db.Column(db.Integer, primary_key=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    emp_dept_emps = db.relationship('Dept_emp', backref='employee', lazy=True, cascade='all, delete')
    man_dept_managers = db.relationship('Dept_manager', backref='employee', lazy=True, cascade='all, delete')
    first_name_index = db.Index("first_name", first_name)

    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
    # TODO: Finish the Employees Class to create the table


class Dept_emp(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), nullable=False, primary_key=True)
    dept_no = db.Column(db.CHAR(4), db.ForeignKey('departments.dept_no'), nullable=False, primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    dept_no_index = db.Index("dept_no", dept_no)

    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'dept_no': self.dept_no,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }
    #  TODO: Finish the Dept_emp Class to create the table


class Dept_manager(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), nullable=False, primary_key=True)
    dept_no = db.Column(db.CHAR(4), db.ForeignKey('departments.dept_no'), nullable=False, primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    dept_no_index = db.Index("dept_no", dept_no)

    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'dept_no': self.dept_no,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }

    # TODO: Finish the Dept_manager Class to create the table
    """
    不通过sql语句创建触发器
    
    @staticmethod
    def add_to_title(target, value, initiator):
        tmp = Dept_manager_title()
        tmp.emp_no = target.emp_no
        tmp.from_date = target.from_date
        tmp.to_date = target.to_date
        db.session.add(tmp)
        db.session.commit()

    @staticmethod
    def delete_title(target):
        db.session.query(Dept_manager_title).filter(Dept_manager_title.emp_no == target.emp_no).delete()

db.event.listen(Dept_manager, 'append', Dept_manager.add_to_title)
db.event.listen(Dept_manager, 'remove', Dept_manager.delete_title)
    """


class Titles(db.Model):
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), nullable=False, primary_key=True)
    title = db.Column(db.String(50), nullable=False, primary_key=True)
    from_date = db.Column(db.Date, nullable=False, primary_key=True)
    to_date = db.Column(db.Date, nullable=False)
    titles_ibfk_1 = db.relationship('Employees', backref='Titles', lazy=True, cascade='all, delete')

    # TODO: Finish the Titles Class to create the table

    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'title': self.title,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }


class Dept_manager_title(db.Model):
    emp_no = db.Column(db.Integer, nullable=False, primary_key=True)
    from_date = db.Column(db.Date, nullable=False, primary_key=True)
    to_date = db.Column(db.Date, nullable=False)

    # TODO: Finish the Dept_manager_title Class to create the table

    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }


sql_trigger_insert = text("""CREATE TRIGGER sql_trigger_insert 
                                AFTER INSERT ON DEPT_MANAGER FOR EACH ROW 
                             BEGIN
                                INSERT INTO DEPT_MANAGER_TITLE(EMP_NO,FROM_DATE,TO_DATE) 
                                VALUES(NEW.EMP_NO,NEW.FROM_DATE,NEW.TO_DATE);
                             END;""")

sql_trigger_delete = text("""CREATE TRIGGER sql_trigger_delete
                                AFTER DELETE ON DEPT_MANAGER FOR EACH ROW
                            BEGIN
                                DELETE FROM DEPT_MANAGER_TITLE WHERE EMP_NO = OLD.EMP_NO AND FROM_DATE = OLD.FROM_DATE
                                AND TO_DATE = OLD.TO_DATE;
                            END;""")


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
reader = read_csv_file('./employees.csv')
rows = []
for row in reader:
    employee = Employees(
        emp_no=row['emp_no'],
        birth_date=row['birth_date'],
        first_name=row['first_name'],
        last_name=row['last_name'],
        gender=row['gender'],
        hire_date=row['hire_date']
    )
    rows.append(employee)
session.bulk_save_objects(rows)
session.commit()
# dept_emp插入
# TODO: insert data
reader = read_csv_file('./dept_emp.csv')
rows = []
for row in reader:
    dept_emp = Dept_emp(
        emp_no=row['emp_no'],
        dept_no=row['dept_no'],
        from_date=row['from_date'],
        to_date=row['to_date']
    )
    rows.append(dept_emp)
session.bulk_save_objects(rows)
session.commit()
# dept_manager插入
# TODO: insert data
reader = read_csv_file('./dept_manager.csv')
rows = []
for row in reader:
    dept_manager = Dept_manager(
        emp_no=row['emp_no'],
        dept_no=row['dept_no'],
        from_date=row['from_date'],
        to_date=row['to_date']
    )
    rows.append(dept_manager)
session.bulk_save_objects(rows)
session.commit()
# titles插入
# TODO: insert data
reader = read_csv_file('./titles.csv')
rows = []
for row in reader:
    titles = Titles(
        emp_no=row['emp_no'],
        title=row['title'],
        from_date=row['from_date'],
        to_date=row['to_date']
    )
    rows.append(titles)
session.bulk_save_objects(rows)
session.commit()
