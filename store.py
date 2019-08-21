from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
from db import db

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@post("/category")
def add_category():
    name = request.forms.get("name")
    return db.add_category(name)

@delete("/category/<id:int>")
def delete_category(id):
    return db.delete_Category(id)

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


run(host='localhost', port=7000, debug=True, reloader=True)
