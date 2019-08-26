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
            cursor.execute(sql)
            result = cursor.fetchall()

            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE": 200})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


def add_product(**fields):
    try:
        with conn.cursor() as cursor:
            sql = f"""SELECT * FROM categories WHERE id = {fields["category"]}"""
            cat_exists = cursor.execute(sql)
            if not cat_exists:
                return json.dumps({"STATUS": "ERROR", "MSG": "Category not found", "CODE": 404})

            if not fields["title"] or not fields["descr"] or not fields["price"] or \
               not fields["img_url"]:
                return json.dumps({"STATUS": "ERROR", "MSG": "missing parameters", "CODE": 400})

            sql = f"""SELECT * FROM products WHERE id = {fields["id"]}"""
            result = cursor.execute(sql)

            if not result:
                sql = f"""INSERT INTO products (title, descr, price, img_url, category, favourite) 
                            VALUES ('{fields["title"]}', '{fields["descr"]}', '{fields["price"]}',
                                    '{fields["img_url"]}', '{fields["category"]}', '{fields["favourite"]}')
                        """ 
                cursor.execute(sql)
                conn.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "PRODUCT_ID": cursor.lastrowid, "CODE": 201})

            else:
                for key, value in fields.items():
                    sql = f"""UPDATE products SET {key} = '{value}' WHERE id = {fields["id"]} """ 
                    cursor.execute(sql)
                    conn.commit()

    except Exception as e:
        print(repr(e))
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


def get_product(id):
    try:
        with conn.cursor() as cursor:
            query = f"""SELECT * FROM products WHERE id = {id}"""
            cursor.execute(query)
            result = cursor.fetchone()

            if not result:
                return json.dumps({"STATUS": "ERROR", "MSG": "Product npt found", "CODE": 404})
            else:
                return json.dumps({"STATUS": "SUCCESS", "PRODUCT": result, "CODE": 200})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


def delete_product(id):
    try:
        with conn.cursor() as cursor:
            query = f"""SELECT * FROM products WHERE id = '{id}'"""
            result = cursor.execute(query)

            if not result:
                return json.dumps({"STATUS": "ERROR", "MSG": "Product not found", "CODE": 404})

            sql = f"""DELETE FROM products WHERE id = '{id}'"""
            cursor.execute(sql)
            conn.commit()

            response.status = 201

            return json.dumps({"STATUS": "SUCCESS", "CODE": 201})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


def list_products():
    try:
        with conn.cursor() as cursor:
            query = f"""SELECT * FROM products"""
            cursor.execute(query)
            result = cursor.fetchall()

            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


def list_products_by_category(id):
    try:
        with conn.cursor() as cursor:
            query = f"""SELECT * FROM categories WHERE id = {id}"""
            cat_exists = cursor.execute(query)

            if not cat_exists:
                return json.dumps({"STATUS": "ERROR", "MSG": "Category not found", "CODE": 404})

            query = f"""SELECT * FROM products WHERE category = '{id}'"""
            cursor.execute(query)
            result = cursor.fetchall()

            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})