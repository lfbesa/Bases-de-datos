
#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask('flaskr')
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "test"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

''' # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/flaskr/queries.json'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+"escuchas.find()")
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"

@app.route("/fecha", methods=['GET', 'POST'])
def fecha():
    fecha = request.args.get("fecha")
    results = mongodb.escuchas.find({"fecha":fecha},{"numero":1})
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results

@app.route("/numero", methods=['GET', 'POST'])
def numero():
    numero = request.args.get("numero")
    k = int(request.args.get("k"))
    results = mongodb.escuchas.find({"numero":numero},{"contenido":1}).sort("fecha",-1).limit(k)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results

@app.route("/palabra", methods=['GET', 'POST'])
def palabra():
    palabra = request.args.get("palabra")
    results = mongodb.escuchas.find({'$text':{'$search':palabra}},{"contenido":1, "ciudad":1, "fecha":1,"numero":1})
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results

@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
