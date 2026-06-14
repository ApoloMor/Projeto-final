from flask import render_template, request, redirect
from flask_app import app
from modules.eventos import (
    criar_tabela_eventos,
    cadastrar_evento,
    listar_eventos,
    excluir_evento,
    buscar_evento,
    editar_evento,
    filtrar_eventos_id,
    filtrar_eventos_nome,

)

from modules.clientes import (
    criar_tabela_clientes, 
    cadastrar_cliente,
    listar_clientes,
    excluir_cliente, 
    editar_cliente, 
    buscar_cliente_por_id
)

from modules.produtos import(
    criar_tabela_produtos,
    cadastrar_produtos,
    excluir_produtos,
    listar_produtos,
    buscar_produtos,
    editar_produtos
)

import os

print(os.getcwd())

@app.route("/")
def home():
    return render_template("home.html")


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

@app.route("/eventos/busca", methods=["POST"])
def buscar_eventos():
  busca = request.form["busca"]
  
  if busca.isdigit():
    
        evento = filtrar_eventos_id(busca)
        eventos = [evento] if evento else []
    
  else:
        eventos = filtrar_eventos_nome(busca)
  total_eventos = len(eventos)
  
  return render_template(
      "eventos.html",
      eventos=eventos,
      total_eventos=total_eventos,
      modo="criar"
  )
  
#ROTA DE CLIENTES E SUAS FUNÇÕES

@app.route("/clientes")
def clientes():
    criar_tabela_clientes()

    lista = listar_clientes()

    return render_template(
        "clientes.html", 
        clientes = lista, 
        total_clientes = len(lista), 
        modo="criar"
    )

#ROTA DE PRODUTOS E SUAS FUNÇÕES

@app.route("/produtos")
def produtos():

    criar_tabela_produtos()

    lista = listar_produtos()

    return render_template(
    "produtos.html",
    produtos=lista,
    total_produtos=len(lista),
    modo = "criar"
    )

@app.route("/produtos/criar", methods=["POST"])
def criar_produtos():

    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]

    cadastrar_evento(
        produto,
        tipo,
        preco,
        estoque
    )

    return redirect("/produtos")

@app.route("/produtos/editar/<int:id>", methods=["GET"])
def edicao(id):

    produtos = buscar_produtos(id)
    lista = listar_produtos()

    return render_template("produtos.html", produtos=lista, total_produtos=len(lista), evento_edicao=produtos, modo="editar")


@app.route("/produtos/atualizar/<int:id>", methods=["POST"]) 
def atualizar_produtos(id):
    
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"] 

    editar_evento(
        id,
        produto,
        tipo,
        preco,
        estoque
    )
    return redirect("/produtos")


@app.route("/produtos/excluir/<int:id>", methods=["POST"])
def remover_produtos(id):

    excluir_produtos(id)

    return redirect("/produtos")

#ROTA DE FORNECEDORES E SUAS FUNÇÕES

@app.route("/fornecedores")
def fornecedores():
    return render_template("fornecedores.html")