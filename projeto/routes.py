from flask import render_template
from flask_app import app

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/eventos")
def eventos():
    return render_template("eventos.html")

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html")

@app.route("/fornecedores")
def fornecedores():
    return render_template("fornecedores.html")