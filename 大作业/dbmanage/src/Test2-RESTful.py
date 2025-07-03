from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
id = 22375080
db = pymysql.connect(
    host="rm-2zemok857yc034840vo.mysql.rds.aliyuncs.com",
    user=f"db_{id}",
    password=f"db_{id}",
    database=f"db_{id}",
    port=3306
)

# db = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="dbmanage",
#     port=3306
# )


# 插入数据
@app.route('/api/v1/<table_name>', methods=['POST'])
def insert_data(table_name):
    data = request.json
    rows = data['rows']
    cursor = db.cursor()
    for row in rows:
        keys = ', '.join(row.keys())
        values = ', '.join([f"'{value}'" for value in row.values()])

        sql = f'insert into {table_name}({keys}) values({values})'
        cursor.execute(sql)
        print(sql)
    db.commit()
    return jsonify({'message': 'data inserted successfully'}), 200


# 更新数据
@app.route('/api/v1/<table_name>', methods=['PUT'])
def update_data(table_name):
    data = request.json
    cursor = db.cursor()
    
    set_clause = ', '.join([f"{key} = '{value}'" for key, value in data.items()])
    
    if table_name == 'departments':
        where_clause = f"dept_no = '{data['dept_no']}'"
    elif table_name == 'employees':
        where_clause = f"emp_no = {data['emp_no']}"
    elif table_name == 'dept_emp':
        where_clause = f"emp_no = {data['emp_no']} AND dept_no = '{data['dept_no']}'"
    elif table_name == 'dept_manager':
        where_clause = f"emp_no = {data['emp_no']} AND dept_no = '{data['dept_no']}'"
    elif table_name == 'titles':
        where_clause = f"emp_no = {data['emp_no']} AND title = '{data['title']}' AND from_date = '{data['from_date']}'"
    
    sql = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
    cursor.execute(sql)
    db.commit()
    return jsonify({'message': 'row updated successfully'}), 200


# 删除数据
@app.route('/api/v1/<table_name>/<path:args>', methods=['DELETE'])
def delete_data(table_name, args):
    cursor = db.cursor()
    
    if table_name == 'departments':
        where_clause = f"dept_no = '{args}'"
    elif table_name == 'employees':
        where_clause = f"emp_no = {args}"
    elif table_name == 'dept_emp':
        emp_no, dept_no = args.split('/')
        where_clause = f"emp_no = {emp_no} AND dept_no = '{dept_no}'"
    elif table_name == 'dept_manager':
        emp_no, dept_no = args.split('/')
        where_clause = f"emp_no = {emp_no} AND dept_no = '{dept_no}'"
    elif table_name == 'titles':
        emp_no, title, from_date = args.split('/')
        where_clause = f"emp_no = {emp_no} AND title = '{title}' AND from_date = '{from_date}'"
    
    sql = f'DELETE FROM {table_name} WHERE {where_clause}'
    cursor.execute(sql)
    db.commit()
    return jsonify({'message': 'row deleted successfully'}), 200


@app.route('/api/v1/<table_name>/<path:args>', methods=['GET'])
def select_data(table_name, args):
    cursor = db.cursor()
    
    if table_name == 'departments':
        where_clause = f"dept_no = '{args}'"
    elif table_name == 'employees':
        where_clause = f"emp_no = {args}"
    elif table_name == 'dept_emp':
        emp_no, dept_no = args.split('/')
        where_clause = f"emp_no = {emp_no} AND dept_no = '{dept_no}'"
    elif table_name == 'dept_manager':
        emp_no, dept_no = args.split('/')
        where_clause = f"emp_no = {emp_no} AND dept_no = '{dept_no}'"
    elif table_name == 'titles':
        emp_no, title, from_date = args.split('/')
        where_clause = f"emp_no = {emp_no} AND title = '{title}' AND from_date = '{from_date}'"
    
    sql = f'SELECT * FROM {table_name} WHERE {where_clause}'
    cursor.execute(sql)
    result = cursor.fetchall()
    return jsonify(result), 200


@app.route('/api/v1/<table_name>', methods=['GET'])
def select_data_condition(table_name):
    cursor = db.cursor()
    conditions = request.args.to_dict()
    
    if not conditions:
        sql = f'SELECT * FROM {table_name}'
    else:
        where_clause = ' AND '.join([f"{key} = '{value}'" for key, value in conditions.items()])
        sql = f'SELECT * FROM {table_name} WHERE {where_clause}'
    
    cursor.execute(sql)
    result = cursor.fetchall()
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=False, port=5555, host='0.0.0.0')
