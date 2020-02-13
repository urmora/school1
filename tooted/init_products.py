# -*- coding: utf-8 -*-

import sqlite3

from flask import Flask

app = Flask(__name__)

DATABASE = 'products.db'

def init_db():
    with app.app_context():
        db = sqlite3.connect(DATABASE)
        with app.open_resource('products.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()