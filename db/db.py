import pymysql, json
from bottle import response

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='Gojuryu2',
                       db='store',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)

def add_category(name):
    if not name:
        return json.dumps({"STATUS": "ERROR", "CODE": 400, "MSG": "Name parameter is missing"})
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT name FROM categories WHERE name = '{name}'"
            result = cursor.execute(sql)
            print(result)
            if result:
                return json.dumps({"STATUS": "ERROR", "CODE": 200, "MSG": "Category already exists"})
            sql = f"INSERT INTO categories (name) VALUES ('{name}')"
            cursor.execute(sql)
            conn.commit()
            id = cursor.lastrowid
            response.status = 201
            code = 201
            status = "SUCCESS"
            return json.dumps({"STATUS": status, "CAT_ID": id, "CODE": code})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "CODE": 500, "MSG": repr(e)})


def delete_Category(id):
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT id FROM categories WHERE id = '{id}'"
            result = cursor.execute(sql)
            print(result)
            if not result:
                return json.dumps({"STATUS": "ERROR", "CODE": 404, "MSG": "Category not found"})
            sql = f"DELETE FROM categories WHERE id ='{id}'"
            cursor.execute(sql)
            conn.commit()
            response.status = 201
            code = 201
            status = "SUCCESS"
            return json.dumps({"STATUS": status, "CODE": code, "MSG": "Category deleted successfully"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "CODE": 500, "MSG": repr(e)})


def list_categories():
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM categories"
            result = cursor.execute(sql)
            print(result)
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE": 200})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})