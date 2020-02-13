# -*- coding: utf-8 -*-

import sqlite3
import json
from flask import ( Flask, g, render_template, jsonify )

app = Flask(
        __name__,
        static_url_path='',
        static_folder='web/'
    )

DATABASE = 'salary.db'

def get_db():
    cn = getattr(g, '_database', None)
    if cn is None:
        cn = g._database = sqlite3.connect(DATABASE)
        cn.row_factory = sqlite3.Row
    return cn.cursor()

# Rakenduse esileht, staatiline HTML
@app.route('/')
def root():
    return app.send_static_file('index.html')

# Tagastab tööperede nimekirja
@app.route('/api/families')
def families_list():
    data = get_db().execute('select id, name from job_family order by name').fetchall()
    return jsonify([dict(ix) for ix in data])

# Tagastab ühe tööpere ametid
@app.route('/api/families/<id>/positions')
def positions_list(id):
    data = get_db().execute('select * from job_position where job_family_id = ?', [id]).fetchall()
    return jsonify([dict(ix) for ix in data])

@app.teardown_appcontext
def close_connection(exception):
    cn = getattr(g, '_database', None)
    if cn is not None:
        cn.close()
