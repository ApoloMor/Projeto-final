from flask import render_template, request, redirect
from flask_app import app
from modules.eventos import (
    criar_tabela_eventos,
    cadastrar_evento,
    listar_eventos,
    excluir_evento,
    buscar_evento,
    editar_evento,
)

from modules.clientes import (
    criar_tabela_clientes, 
    cadastrar_cliente,
    listar_clientes,
    excluir_cliente, 
    editar_cliente
)

from modules.produtos import(
    criar_tabela_produtos,
    cadastrar_produtos,
    excluir_produtos
)

import os

print(os.getcwd())

@app.route("/")
def home():
    return render_template("Home.html")


#ROTA DE EVENTOS E SUAS FUNÇÕES

@app.route("/eventos")
def eventos():

    criar_tabela_eventos()

    lista = listar_eventos()

    return render_template(
    "eventos.html",
    eventos=lista,
    total_eventos=len(lista),
    modo = "criar"
)

@app.route("/eventos/criar", methods=["POST"])
def criar_evento():

    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"]

    cadastrar_evento(
        nome,
        jogo,
        data,
        vagas
    )

    return redirect("/eventos")


@app.route("/eventos/editar/<int:id>", methods=["GET"])
def mostrar_edicao(id):

    evento = buscar_evento(id)
    lista = listar_eventos()

    return render_template("eventos.html", eventos=lista, total_eventos=len(lista), evento_edicao=evento, modo="editar")


@app.route("/eventos/atualizar/<int:id>", methods=["POST"]) #Receber id ↓Receber request.form ↓Chamar editar_evento(...) ↓redirect("/eventos")
def atualizar_eventos(id):
    
    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"] 

    editar_evento(
        id,
        nome,
        jogo,
        data,
        vagas
    )
    return redirect("/eventos")


@app.route("/eventos/excluir/<int:id>", methods=["POST"])
def remover_evento(id):

    excluir_evento(id)

    return redirect("/eventos")

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/produtos")
def produtos():



    return render_template("produtos.html")

@app.route("/fornecedores")
def fornecedores():
    return render_template("fornecedores.html")