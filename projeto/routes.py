from flask import render_template, request, redirect
from flask_app import app
from collections import Counter

from modules.eventos import (
    carregar_eventos,
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
    verificar_data,
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
    editar_inscricao,
)

from modules.produtos import(
    criar_tabela_produtos,
    cadastrar_produtos,
    excluir_produtos,
    listar_produtos,
    buscar_produtos,
    editar_produtos,
    buscar_produtos_nome,
    buscar_produtos_por_tipo,
    entrada_estoque,
    saida_estoque,
    criar_tabela_movimentacoes,   
    listar_todas_movimentacoes,
    produtos_mais_vendidos,
)

from modules.fornecedores import (
    criar_tabela_fornecedores,
    cadastrar_fornecedor,
    listar_fornecedores,
    buscar_fornecedor,
    editar_fornecedor,
    excluir_fornecedor,
)

import os
from datetime import datetime

print(os.getcwd())


def calcular_dados_produtos(lista):
    total_produtos = len(lista)
    valor_total = sum(p[3] * p[4] for p in lista) if lista else 0
    produtos_alerta = len([p for p in lista if p[4] <= 20])
    produto_mais_caro = max(lista, key=lambda p: p[3], default=None)
    maior_estoque = max(lista, key=lambda p: p[4], default=None)
    categorias = Counter(p[2] for p in lista) if lista else {}
    categorias_labels = list(categorias.keys())
    categorias_valores = list(categorias.values())

    return {
        "total_produtos": total_produtos,
        "valor_total": valor_total,
        "produtos_alerta": produtos_alerta,
        "produto_mais_caro": produto_mais_caro,
        "maior_estoque": maior_estoque,
        "categorias_labels": categorias_labels,
        "categorias_valores": categorias_valores,
    }


# ROTA DE INSCREVER CLIENTES >> EVENTO

@app.route("/")
def home():

    criar_tabela_inscricoes()

    lista = listar_inscricoes()

    return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
)   

@app.route("/inscricoes", methods=["POST"])
def inscrever():

    lista = listar_inscricoes()

    id_cliente = request.form["id_cliente"]
    id_evento = request.form["id_evento"]
    
    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Cliente não encontrado!",
        )
    
    evento = filtrar_eventos_id(id_evento)
    if not evento:
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Evento não encontrado!",
        )
    
    elif evento_lotado(id_evento):
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Evento lotado!",
        )
    
    else:
        inscrever_cliente_evento(id_cliente, id_evento)

    return redirect("/")

@app.route("/inscricoes/editar", methods=["GET"])
def edicao_inscricao(id,):

    inscricao = buscar_inscricao(id)
    lista = listar_inscricoes()

    return render_template(
        "home.html", 
        inscricao=lista, 
        modo="editar")


@app.route("/inscricoes/atualizar/<int:id>", methods=["POST"]) #Receber id ↓Receber request.form ↓Chamar editar_evento(...) ↓redirect("/eventos")
def atualizar_inscricao(id):
    
    lista = listar_inscricoes()

    id_cliente = request.form["id_cliente"]
    id_evento = request.form["id_evento"]

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Cliente não encontrado!",
        )
    
    evento = filtrar_eventos_id(id_evento)
    
    if not evento:
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Evento não encontrado!",
        )
    
    elif evento_lotado(id_evento):
        return render_template(
            "home.html",
            inscricoes = lista,
            modo_insc = "criar",
            modo_vnd = "criar",
            error = "Evento lotado!",
        )
    
    editar_evento(
        id,
        id_cliente,
        id_cliente
    )

    return redirect("/")

@app.route("/inscricoes/excluir/<int:id>", methods=["POST"])
def remover_inscricao(id):
    excluir_inscricao(id)
    return redirect("/")


# ROTA DE EVENTOS E SUAS FUNÇÕES

@app.route("/eventos")
def eventos():
    criar_tabela_eventos()

    eventos = carregar_eventos()

    return render_template(
        "eventos.html",
        eventos=eventos,
        total_eventos = len(eventos),
        modo = "criar",
)

@app.route("/eventos/criar", methods=["POST"])
def criar_evento():

    eventos = carregar_eventos()

    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"]

    if verificar_data(data):
        return render_template(
        "eventos.html",
        eventos=eventos,
        total_eventos=len(eventos),
        modo = "criar",
        error = "Data inválida!"
)
    
    else:
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

    return render_template(
        "eventos.html", 
        eventos=lista, 
        total_eventos=len(lista), 
        evento_edicao=evento, 
        modo="editar")


@app.route("/eventos/atualizar/<int:id>", methods=["POST"])
def atualizar_eventos(id):
    
    eventos = carregar_eventos()

    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"] 

    if verificar_data(data):
        return render_template(
        "eventos.html",
        eventos=eventos,
        total_eventos = len(eventos),
        modo = "criar",
        error ="Data inválida!"
        )
    else:

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
    return render_template("eventos.html", eventos=eventos, total_eventos=len(eventos), modo="criar")


# ROTA DE CLIENTES E SUAS FUNÇÕES

@app.route("/clientes")
def clientes():
    criar_tabela_clientes()
    lista = listar_clientes()
    return render_template("clientes.html", clientes=lista, total_clientes=len(lista), modo="criar")


@app.route("/clientes/criar", methods=["POST"])
def criar_cliente():
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
    return render_template("clientes.html", clientes=lista, total_clientes=len(lista), cliente_edicao=cliente, modo="editar")


@app.route("/clientes/atualizar/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    editar_cliente(id, nome, cpf, telefone, email)
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

    return render_template("clientes.html", clientes=lista, total_clientes=len(lista), modo="criar")


# ROTA DE PRODUTOS E SUAS FUNÇÕES

@app.route("/produtos")
def produtos():
    criar_tabela_produtos()
    criar_tabela_movimentacoes() 
    lista = listar_produtos()
    dados = calcular_dados_produtos(lista)
    historico = listar_todas_movimentacoes() 
    mais_vendidos = produtos_mais_vendidos()  

    return render_template("produtos.html", produtos=lista, modo="criar",
                           historico=historico, mais_vendidos=mais_vendidos, **dados)

@app.route("/produtos/criar", methods=["POST"])
def criar_produtos():
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    cadastrar_produtos(produto, tipo, preco, estoque)
    return redirect("/produtos")


@app.route("/produtos/editar/<int:id>", methods=["GET"])
def edicao(id):
    produto = buscar_produtos(id)
    lista = listar_produtos()
    dados = calcular_dados_produtos(lista)

    return render_template("produtos.html", produtos=lista, produto_edicao=produto, modo="editar", **dados)


@app.route("/produtos/atualizar/<int:id>", methods=["POST"])
def atualizar_produtos(id):
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    editar_produtos(id, produto, tipo, preco, estoque)
    return redirect("/produtos")


@app.route("/produtos/excluir/<int:id>", methods=["POST"])
def remover_produtos(id):
    excluir_produtos(id)
    return redirect("/produtos")


@app.route("/produtos/busca", methods=["POST"])
def buscar_produtos_route():
    busca = request.form["busca"]
    if busca.isdigit():
        produto = buscar_produtos(int(busca))
        lista = [produto] if produto else []
    else:
        lista = buscar_produtos_nome(busca)
    dados = calcular_dados_produtos(lista)

    return render_template("produtos.html", produtos=lista, modo="criar", **dados)


@app.route("/produtos/busca-tipo", methods=["POST"])
def buscar_produtos_tipo():
    tipo = request.form["tipo"]
    lista = buscar_produtos_por_tipo(tipo)
    dados = calcular_dados_produtos(lista)

    return render_template("produtos.html", produtos=lista, modo="criar", **dados)

@app.route("/produtos/entrada/<int:id>", methods=["POST"])
def entrada_produto(id):
    quantidade = int(request.form["quantidade"])
    entrada_estoque(id, quantidade)
    return redirect("/produtos")

@app.route("/produtos/saida/<int:id>", methods=["POST"])
def saida_produto(id):
    quantidade = int(request.form["quantidade"])
    saida_estoque(id, quantidade)
    return redirect("/produtos")


# ROTA DE FORNECEDORES E SUAS FUNÇÕES

@app.route("/fornecedores")
def fornecedores():
    criar_tabela_fornecedores()
    lista = listar_fornecedores()
    return render_template(
        "fornecedores.html",
        fornecedores=lista,
        total_fornecedores=len(lista),
        modo="criar"
    )


@app.route("/fornecedores/criar", methods=["POST"])
def criar_fornecedor_route():
    nome = request.form["nome"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    cadastrar_fornecedor(nome, cnpj, telefone, email)
    return redirect("/fornecedores")


@app.route("/fornecedores/editar/<int:id>", methods=["GET"])
def editar_fornecedor_route(id):
    criar_tabela_fornecedores()
    fornecedor = buscar_fornecedor(id)
    lista = listar_fornecedores()
    return render_template(
        "fornecedores.html",
        fornecedores=lista,
        total_fornecedores=len(lista),
        fornecedor_edicao=fornecedor,
        modo="editar"
    )


@app.route("/fornecedores/atualizar/<int:id>", methods=["POST"])
def atualizar_fornecedor(id):
    nome = request.form["nome"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    editar_fornecedor(id, nome, cnpj, telefone, email)
    return redirect("/fornecedores")


@app.route("/fornecedores/excluir/<int:id>", methods=["POST"])
def remover_fornecedor(id):
    excluir_fornecedor(id)
    return redirect("/fornecedores")