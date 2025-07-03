import json

from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
id = 22371437
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
    return jsonify({'message': 'data inserted successfully'})


# 更新数据
@app.route('/api/v1/<table_name>', methods=['PUT'])
def update_data(table_name):
    data = request.json
    # 获取列和数据
    keys = list(data.keys())
    values = list(data.values())
    cursor = db.cursor()
    # 获取主键名称
    cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
    primary_key_columns = [row[4] for row in cursor.fetchall()]

    i = 0
    where = ""
    for key in keys:
        for primary_key in primary_key_columns:
            if key == primary_key:
                where += key + " = '" + str(values[i]) + "'"
        keys[i] = key + " = '" + str(values[i]) + "'"
        i = 1 + i
    word = ' ,'.join(keys)
    sql = f'update {table_name} set {word} where {where}'
    cursor.execute(sql)
    db.commit()
    return jsonify({'message': 'data updated successfully'})


# TODO: finish this fuction to update data


# 删除数据
@app.route('/api/v1/<table_name>/<path:args>', methods=['DELETE'])
def delete_data(table_name, args):
    cursor = db.cursor()
    args = args.split('/')
    cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
    primary_key_columns = [row[4] for row in cursor.fetchall()]

    for i in range(len(primary_key_columns)):
        primary_key_columns[i] += " = '" + args[i] + "'"

    where = ' and '.join(primary_key_columns)
    sql = f"delete from {table_name} where {where}"
    cursor.execute(sql)
    db.commit()
    return jsonify({'message': 'data deleted successfully'})
    # TODO: finish this fuction to update data


@app.route('/api/v1/<table_name>/<path:args>', methods=['GET'])
def select_data(table_name, args):
    cursor = db.cursor()
    # 获取主键数据
    args = args.split('/')
    cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
    primary_key_columns = [row[4] for row in cursor.fetchall()]

    for i in range(len(primary_key_columns)):
        primary_key_columns[i] += " = '" + args[i] + "'"

    # 如果有多个主键用 and 连接
    where = ' and '.join(primary_key_columns)
    sql = f"select * from {table_name} where {where}"
    cursor.execute(sql)
    datas = [row for row in cursor.fetchall()]
    # 将数据转化为字符串进行输出
    strs = []
    for row in datas:
        string = []
        for data in row:
            string.append(str(data))
        strs.append(', '.join(string))

    db.commit()
    return jsonify({'data': f'{data}' for data in strs})

    # TODO: finish this fuction to update data


@app.route('/api/v1/<table_name>', methods=['GET'])
def select_data_condition(table_name):
    global filter_column, filter_value
    cursor = db.cursor()

    # 获取筛选条件
    string = request.args.to_dict()
    for i in string.keys():
        filter_column = i
    for i in string.values():
        filter_value = i

    # 分是否有筛选条件的情况进行讨论
    if filter_column and filter_value:
        sql = f"select * from {table_name} where {filter_column} = {filter_value}"
    else:
        sql = f"select * from {table_name}"

    cursor.execute(sql)
    datas = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    data = []
    for row in datas:
        row_data = {}
        for i in range(len(columns)):
            row_data[columns[i]] = str(row[i])
        data.append(row_data)
    db.commit()
    return jsonify({'data': f'{data}'})
    # TODO: finish this fuction to update data


if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
