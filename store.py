from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
from db import db


@get("/")
def index():
    return template("index.html")

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/categories")
def list_categories():
    return db.list_categories()

@post("/category")
def add_category():
    name = request.forms.get("name")
    return db.add_category(name)

@delete("/category/<id:int>")
def delete_category(id):
    return db.delete_Category(id)

@post("/product")
def add_or_edit_product():
    id = request.forms.get("id")
    title = request.forms.get("title")
    desc = request.forms.get("desc")
    price = request.forms.get("price")
    img_url = request.forms.get("img_url")
    category = request.forms.get("category")
    favourite = request.forms.get("favorite")

    if not favourite:
        favourite = 0
    else:
        favourite = 1
    
    return db.add_product(id=id, title=title, desc=desc, price=price, img_url=img_url, category=category, \
                          favourite=favourite)

@get("/product/<id:int>")
def get_product(id):
    return db.get_product(id)

@delete("/product/<id:int>")
def delete_product(id):
    return 


run(host='localhost', port=7000, debug=True, reloader=True)
