from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
id = 22370000
db = pymysql.connect(
    host="119.3.248.160",
    user=f"{id}",
    password=f"{id}",
    database=f"db_{id}",
    port=3306
)


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
    db.commit()
    return jsonify({'message': 'data inserted successfully'}), 201


# 更新数据
@app.route('/api/v1/<table_name>', methods=['PUT'])
def update_data(table_name):


# TODO: finish this fuction to update data


# 删除数据
@app.route('/api/v1/<table_name>/<path:args>', methods=['DELETE'])
def delete_data(table_name, args):


# TODO: finish this fuction to update data


@app.route('/api/v1/<table_name>/<path:args>', methods=['GET'])
def select_data(table_name, args):


# TODO: finish this fuction to update data


@app.route('/api/v1/<table_name>', methods=['GET'])
def select_data_condition(table_name):


# TODO: finish this fuction to update data


if __name__ == '__main__':
    app.run(debug=False, port=5555, host='0.0.0.0')
