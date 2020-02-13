# -*- coding: utf-8 -*-

import sqlite3
import json
from flask import ( Flask, g )

app = Flask(__name__)

# Kus asub SQLite andmebaasi fail, täpsemalt edaspidi sellest
DATABASE = 'products.db'

# Avame andmebaasi faili
def get_db():
    cn = getattr(g, '_database', None)
    if cn is None:
        cn = g._database = sqlite3.connect(DATABASE)
        cn.row_factory = sqlite3.Row
    return cn.cursor()

# See on tegelik API "entry point" ehk koht millele veebirakendus vastab tagastades toodete nimekirja JSON formaadis
@app.route('/products')
def product_list():
    db = get_db()
    data = db.execute('select id, name from products order by name').fetchall()
    return json.dumps( [dict(ix) for ix in data] )
   
# Rakenduse töö lõppedes on tähtis andmebaasi fail sulgeda
@app.teardown_appcontext
def close_connection(exception):
    cn = getattr(g, '_database', None)
    if cn is not None:
        cn.close()
