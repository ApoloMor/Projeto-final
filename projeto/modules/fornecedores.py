from app import app
from flask import render_template
import sqlite3

@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html')