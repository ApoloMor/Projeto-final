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
    filtrar_eventos_jogo,
    obter_status_evento,
)

from modules.clientes import (
    criar_tabela_clientes, 
    cadastrar_cliente,
    listar_clientes,
    excluir_cliente, 
    editar_cliente, 
    buscar_cliente_por_id,
    buscar_cliente,
    buscar_cliente_nome
)

from modules.inscricoes import (
    criar_tabela_inscricoes,
    listar_inscricoes,
    inscrever_cliente_evento,
    contar_participantes,
    buscar_vagas_evento,
    vagas_disponiveis,
    evento_lotado,
    excluir_inscricao,
    buscar_inscricao,
)

from modules.produtos import(
    criar_tabela_produtos,
    cadastrar_produtos,
    excluir_produtos,
    listar_produtos,
    buscar_produtos,
    editar_produtos,
)

import os

print(os.getcwd())

#ROTA DE ISCREVER CLIENTES >> EVENTO

@app.route("/")
def home():
    criar_tabela_inscricoes()

    lista = listar_inscricoes()

    return render_template(
            "home.html",
            inscricoes = lista
)  

@app.route("/inscricoes", methods=["POST"])
def inscrever():

    id_cliente = request.form["id_cliente"]
    id_evento = request.form["id_evento"]
    
    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return "Cliente não encontrado"
    
    evento = filtrar_eventos_id(id_evento)
    
    if not evento:
        return "Evento não encontrado"
    
    elif evento_lotado(id_evento):
        return "Evento lotado!"
    
    else:
        inscrever_cliente_evento(id_cliente, id_evento)

    return redirect("/")

@app.route("/inscricoes/excluir/<int:id>", methods=["POST"])
def remover_inscricao(id):

    excluir_inscricao(id)

    return redirect("/")


#ROTA DE EVENTOS E SUAS FUNÇÕES

@app.route("/eventos")
def eventos():

    criar_tabela_eventos()

    lista = listar_eventos()

    eventos_com_status = [] #outra lista para nn mecher no banco de dados, pois nn fizemos uma coluna status de verdade

    for evento in lista:

        vagas = vagas_disponiveis(evento[0])
        status = obter_status_evento(
            evento[3],#data
            vagas_disponiveis(evento[0])#vagas
        )

        evento = list(evento)
        evento.append(vagas)
        evento.append(status)

        eventos_com_status.append(evento)

    return render_template(
    "eventos.html",
    eventos=eventos_com_status,
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

@app.route("/eventos/busca-tipo", methods=["POST"])
def buscar_eventos_tipo():
  
  tipo = request.form["tipo"]
  eventos = filtrar_eventos_jogo(tipo)
  total_eventos=len(eventos)

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

@app.route("/clientes/criar", methods=["POST"])
def criar_cliente(): #request.form eh pra preencher auto com os dados que vieram do html
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    email = request.form["email"]

    cadastrar_cliente(nome, cpf, telefone, email)

    return redirect("/clientes")

@app.route("/clientes/editar/<int:id>", methods=["GET"])
def mostrar_edicao_cliente(id):
    cliente = buscar_cliente_por_id(id)
    lista = listar_clientes()

    return render_template(
        "clientes.html",
        clientes=lista, 
        total_clientes=len(lista),
        cliente_edicao=cliente,
        modo="editar"
    )

@app.route("/clientes/atualizar/<int:id>", methods=["POST"])
def atualizar_cliente(id):

    nome = request.form["nome"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    email = request.form["email"]

    editar_cliente(
        id, 
        nome, 
        cpf, 
        telefone, 
        email
    )
    return redirect("/clientes")

@app.route("/clientes/excluir/<int:id>", methods=["POST"])
def remover_cliente(id):
    excluir_cliente(id)
    return redirect("/clientes")

@app.route("/clientes/buscar", methods=["POST"])
def buscar_cliente_route():
    tipo = request.form["tipo_busca"]
    termo = request.form["termo"]

    if tipo == "nome":
        lista = buscar_cliente_nome(termo)
    elif tipo == "cpf":
        resultado = buscar_cliente(termo)
        lista = [resultado] if resultado else []
    elif tipo == "id":
        resultado = buscar_cliente_por_id(int(termo))
        lista = [resultado] if resultado else []
    else:
        lista = listar_clientes()

    return render_template(
        "clientes.html",
        clientes=lista,
        total_clientes=len(lista),
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
    modo="criar"
)

@app.route("/produtos/criar", methods=["POST"])
def criar_produtos():

    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]

    cadastrar_produtos(
        produto,
        tipo,
        preco,
        estoque
    )

    return redirect("/produtos")

@app.route("/produtos/editar/<int:id>", methods=["GET"])
def edicao(id):

    produto = buscar_produtos(id)
    lista = listar_produtos()

    return render_template(
        "produtos.html",
        produtos=lista,
        total_produtos=len(lista),
        produto_edicao=produto,
        modo="editar"
    )


@app.route("/produtos/atualizar/<int:id>", methods=["POST"]) 
def atualizar_produtos(id):
    
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"] 

    editar_produtos(
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