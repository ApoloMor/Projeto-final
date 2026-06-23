from flask import render_template, request, redirect
from flask_app import app
from collections import Counter
from datetime import datetime
import os

import functools
from flask import render_template, request, redirect, session
from modules.vendas import criar_tabela_vendas, registrar_venda, listar_vendas

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
    adicionar_status_eventos,
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
    buscar_cliente_nome,
)

from modules.inscricoes import (
    criar_tabela_inscricoes,
    listar_inscricoes,
    ja_inscrito,
    inscrever_cliente_evento,
    evento_lotado,
    excluir_inscricao,
    buscar_inscricao_por_id,
    editar_inscricao,
    total_clientes_inscritos,
    filtrar_inscricao_id,
    filtrar_cliente_nome,
    filtrar_eventos_nome_insc,
    filtrar_eventos_tipo_insc,
    carregar_inscricoes,
    adicionar_nomes,
    total_eventos_com_vagas,
    contar_inscricoes,
)

from modules.produtos import (
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
    buscar_fornecedor_nome,
    buscar_fornecedor_cnpj,
)

from modules.vendas import (
    criar_tabela_vendas,
    registrar_venda,
    listar_vendas,
)

from modules.reutilizaveis import (
    paginar,
)

print(os.getcwd())


def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logado'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logado'):
        return redirect('/')
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '1234':
            session['logado'] = True
            return redirect('/')
        return render_template('login.html', error='Usuário ou senha incorretos.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


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


def render_home(lista, **kwargs):
    dados = paginar(lista, 5)
    return render_template(
        "home.html",
        inscricoes=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_inscricoes=len(lista),
        total_clientes=total_clientes_inscritos(),
        eventos_abertos=total_eventos_com_vagas(),
        eventos_existentes=len(listar_eventos()),
        clientes_existentes=len(listar_clientes()),
        modo_insc="criar",
        modo_vnd="criar",
        em_busca=False,
        **kwargs
    )


# ==================== HISTÓRICO ====================

@app.route("/historico")
@login_required
def historico():
    criar_tabela_vendas()
    vendas = listar_vendas()
    faturamento = sum(v[3] * v[4] for v in vendas) if vendas else 0
    return render_template(
        "historico.html",
        vendas=vendas,
        total_vendas=len(vendas),
        faturamento=faturamento
    )


# ==================== HOME / INSCRIÇÕES ====================

@app.route("/")
@login_required
def home():
    criar_tabela_inscricoes()
    lista = carregar_inscricoes()
    return render_home(lista)


@app.route("/inscricoes", methods=["POST"])
@login_required
def inscrever():
    lista = carregar_inscricoes()
    id_cliente = request.form["id_cliente"]
    id_evento = request.form["id_evento"]

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return render_home(lista, error="Cliente não encontrado!")

    evento = filtrar_eventos_id(id_evento)
    if not evento:
        return render_home(lista, error="Evento não encontrado!")

    if evento_lotado(id_evento):
        return render_home(lista, error="Evento lotado!")

    if ja_inscrito(id_cliente, id_evento):
        return render_home(lista, error="Cliente já inscrito neste evento!")

    inscrever_cliente_evento(id_cliente, id_evento)
    lista = carregar_inscricoes()
    return render_home(lista, success="Cliente inscrito no evento com sucesso!")


@app.route("/inscricoes/editar/<int:id>", methods=["GET"])
@login_required
def edicao_inscricao(id):
    inscricao = buscar_inscricao_por_id(id)
    lista = carregar_inscricoes()
    dados = paginar(lista, 5)
    return render_template(
        "home.html",
        inscricoes=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_inscricoes=len(lista),
        total_clientes=total_clientes_inscritos(),
        eventos_abertos=total_eventos_com_vagas(),
        eventos_existentes=len(listar_eventos()),
        clientes_existentes=len(listar_clientes()),
        inscricao=inscricao,
        modo_insc="editar",
        modo_vnd="criar",
        em_busca=False
    )


@app.route("/inscricoes/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_inscricao(id):
    lista = carregar_inscricoes()
    id_evento = request.form["id_evento"]
    evento = filtrar_eventos_id(id_evento)

    if not evento:
        return render_home(lista, error="Evento não encontrado!")
    elif evento_lotado(id_evento):
        return render_home(lista, error="Evento lotado!")

    editar_inscricao(id, id_evento)
    return redirect("/")


@app.route("/inscricoes/excluir/<int:id>", methods=["POST"])
@login_required
def remover_inscricao(id):
    excluir_inscricao(id)
    return redirect("/")


@app.route("/inscricoes/busca", methods=["POST"])
@login_required
def buscar_inscricao():
    busca = request.form["busca"]
    if busca.isdigit():
        inscricao = filtrar_inscricao_id(busca)
        inscricoes = [inscricao] if inscricao else []
    else:
        inscricoes = filtrar_cliente_nome(busca)
        if not inscricoes:
            inscricoes = filtrar_eventos_nome_insc(busca)
    inscricoes = adicionar_nomes(inscricoes)
    return render_template(
        "home.html",
        inscricoes=inscricoes,
        total_inscricoes=len(inscricoes),
        total_clientes=total_clientes_inscritos(),
        eventos_abertos=total_eventos_com_vagas(),
        eventos_existentes=len(listar_eventos()),
        clientes_existentes=len(listar_clientes()),
        modo_insc="criar",
        modo_vnd="criar",
        em_busca=True
    )


@app.route("/inscricoes/busca-tipo", methods=["POST"])
@login_required
def buscar_inscricao_tipo():
    tipo = request.form["tipo"]
    inscricoes = filtrar_eventos_tipo_insc(tipo)
    inscricoes = adicionar_nomes(inscricoes)
    return render_template(
        "home.html",
        inscricoes=inscricoes,
        total_inscricoes=len(inscricoes),
        total_clientes=total_clientes_inscritos(),
        eventos_abertos=total_eventos_com_vagas(),
        eventos_existentes=len(listar_eventos()),
        clientes_existentes=len(listar_clientes()),
        modo_insc="criar",
        modo_vnd="criar",
        em_busca=True
    )


# ==================== EVENTOS ====================

@app.route("/eventos")
@login_required
def eventos():
    criar_tabela_eventos()
    eventos = carregar_eventos()
    dados = paginar(eventos, 5)
    return render_template(
        "eventos.html",
        eventos=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_eventos=len(eventos),
        modo="criar",
        em_busca=False
    )


@app.route("/eventos/criar", methods=["POST"])
@login_required
def criar_evento():
    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"]
    eventos = carregar_eventos()
    dados = paginar(eventos, 5)

    if verificar_data(data):
        return render_template(
            "eventos.html",
            eventos=dados["itens"],
            pagina=dados["pagina"],
            total_paginas=dados["total_paginas"],
            total_eventos=len(eventos),
            modo="criar",
            error="Data inválida!",
            em_busca=False
        )

    cadastrar_evento(nome, jogo, data, vagas)
    eventos = carregar_eventos()
    dados = paginar(eventos, 5)
    return render_template(
        "eventos.html",
        eventos=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_eventos=len(eventos),
        modo="criar",
        success="Evento cadastrado!",
        em_busca=False
    )


@app.route("/eventos/editar/<int:id>", methods=["GET"])
@login_required
def mostrar_edicao(id):
    evento = buscar_evento(id)
    eventos = carregar_eventos()
    dados = paginar(eventos, 5)
    return render_template(
        "eventos.html",
        eventos=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_eventos=len(eventos),
        evento_edicao=evento,
        modo="editar",
        em_busca=False
    )


@app.route("/eventos/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_eventos(id):
    nome = request.form["nome"]
    jogo = request.form["jogo"]
    data = request.form["data"]
    vagas = request.form["vagas"]
    eventos = carregar_eventos()
    dados = paginar(eventos, 5)

    if verificar_data(data):
        return render_template(
            "eventos.html",
            eventos=dados["itens"],
            pagina=dados["pagina"],
            total_paginas=dados["total_paginas"],
            total_eventos=len(eventos),
            modo="criar",
            error="Data inválida!",
            em_busca=False
        )
    if int(vagas) < contar_inscricoes(id):
        return render_template(
            "eventos.html",
            eventos=dados["itens"],
            pagina=dados["pagina"],
            total_paginas=dados["total_paginas"],
            total_eventos=len(eventos),
            modo="criar",
            error="Não pode haver menos vagas que inscritos!",
            em_busca=False
        )

    editar_evento(id, nome, jogo, data, vagas)
    return redirect("/eventos")


@app.route("/eventos/excluir/<int:id>", methods=["POST"])
@login_required
def remover_evento(id):
    excluir_evento(id)
    return redirect("/eventos")


@app.route("/eventos/busca", methods=["POST"])
@login_required
def buscar_eventos():
    busca = request.form["busca"]
    if busca.isdigit():
        evento = filtrar_eventos_id(busca)
        eventos = [evento] if evento else []
    else:
        eventos = filtrar_eventos_nome(busca)
    eventos = adicionar_status_eventos(eventos)
    return render_template(
        "eventos.html",
        eventos=eventos,
        total_eventos=len(eventos),
        modo="criar",
        em_busca=True
    )


@app.route("/eventos/busca-tipo", methods=["POST"])
@login_required
def buscar_eventos_tipo():
    tipo = request.form["tipo"]
    eventos = filtrar_eventos_jogo(tipo)
    eventos = adicionar_status_eventos(eventos)
    return render_template(
        "eventos.html",
        eventos=eventos,
        total_eventos=len(eventos),
        modo="criar",
        em_busca=True
    )


# ==================== CLIENTES ====================

@app.route("/clientes")
@login_required
def clientes():
    criar_tabela_clientes()
    lista = listar_clientes()
    dados = paginar(lista, 5)
    return render_template(
        "clientes.html",
        clientes=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_clientes=len(lista),
        modo="criar",
        em_busca=False
    )


@app.route("/clientes/criar", methods=["POST"])
@login_required
def criar_cliente():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    cadastrar_cliente(nome, cpf, telefone, email)
    return redirect("/clientes")


@app.route("/clientes/editar/<int:id>", methods=["GET"])
@login_required
def mostrar_edicao_cliente(id):
    cliente = buscar_cliente_por_id(id)
    lista = listar_clientes()
    dados = paginar(lista, 5)
    return render_template(
        "clientes.html",
        clientes=dados["itens"],
        pagina=dados["pagina"],
        total_paginas=dados["total_paginas"],
        total_clientes=len(lista),
        cliente_edicao=cliente,
        modo="editar",
        em_busca=False
    )


@app.route("/clientes/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_cliente(id):
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    editar_cliente(id, nome, cpf, telefone, email)
    return redirect("/clientes")


@app.route("/clientes/excluir/<int:id>", methods=["POST"])
@login_required
def remover_cliente(id):
    excluir_cliente(id)
    return redirect("/clientes")


@app.route("/clientes/buscar", methods=["POST"])
@login_required
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
        modo="criar",
        em_busca=True
    )


# ==================== PRODUTOS ====================

@app.route("/produtos")
@login_required
def produtos():
    criar_tabela_produtos()
    criar_tabela_movimentacoes()
    lista = listar_produtos()
    dados = calcular_dados_produtos(lista)
    historico = listar_todas_movimentacoes()
    mais_vendidos = produtos_mais_vendidos()
    dadosPag = paginar(lista, 5)
    return render_template(
        "produtos.html",
        produtos=dadosPag["itens"],
        pagina=dadosPag["pagina"],
        total_paginas=dadosPag["total_paginas"],
        modo="criar",
        historico=historico,
        mais_vendidos=mais_vendidos,
        em_busca=False,
        **dados
    )


@app.route("/produtos/criar", methods=["POST"])
@login_required
def criar_produtos():
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    cadastrar_produtos(produto, tipo, preco, estoque)
    return redirect("/produtos")


@app.route("/produtos/editar/<int:id>", methods=["GET"])
@login_required
def edicao(id):
    produto = buscar_produtos(id)
    lista = listar_produtos()
    dados = calcular_dados_produtos(lista)
    dadosPag = paginar(lista, 5)
    return render_template(
        "produtos.html",
        produtos=dadosPag["itens"],
        pagina=dadosPag["pagina"],
        total_paginas=dadosPag["total_paginas"],
        produto_edicao=produto,
        modo="editar",
        em_busca=False,
        **dados
    )


@app.route("/produtos/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_produtos(id):
    produto = request.form["produto"]
    tipo = request.form["tipo"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    editar_produtos(id, produto, tipo, preco, estoque)
    return redirect("/produtos")


@app.route("/produtos/excluir/<int:id>", methods=["POST"])
@login_required
def remover_produtos(id):
    excluir_produtos(id)
    return redirect("/produtos")


@app.route("/produtos/busca", methods=["POST"])
@login_required
def buscar_produtos_route():
    busca = request.form["busca"]
    if busca.isdigit():
        produto = buscar_produtos(int(busca))
        lista = [produto] if produto else []
    else:
        lista = buscar_produtos_nome(busca)
    dados = calcular_dados_produtos(lista)
    return render_template(
        "produtos.html",
        produtos=lista,
        modo="criar",
        em_busca=True,
        **dados
    )


@app.route("/produtos/busca-tipo", methods=["POST"])
@login_required
def buscar_produtos_tipo():
    tipo = request.form["tipo"]
    lista = buscar_produtos_por_tipo(tipo)
    dados = calcular_dados_produtos(lista)
    return render_template(
        "produtos.html",
        produtos=lista,
        modo="criar",
        em_busca=True,
        **dados
    )


@app.route("/produtos/entrada/<int:id>", methods=["POST"])
@login_required
def entrada_produto(id):
    quantidade = int(request.form["quantidade"])
    entrada_estoque(id, quantidade)
    return redirect("/produtos")


@app.route("/produtos/saida/<int:id>", methods=["POST"])
@login_required
def saida_produto(id):
    quantidade = int(request.form["quantidade"])
    saida_estoque(id, quantidade)
    return redirect("/produtos")


# ==================== FORNECEDORES ====================

@app.route("/fornecedores")
@login_required
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
@login_required
def criar_fornecedor_route():
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    cadastrar_fornecedor(nome, tipo, cnpj, telefone, email, "N/A")
    return redirect("/fornecedores")


@app.route("/fornecedores/editar/<int:id>", methods=["GET"])
@login_required
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
@login_required
def atualizar_fornecedor(id):
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    editar_fornecedor(id, nome, tipo, cnpj, telefone, email, "N/A")
    return redirect("/fornecedores")


@app.route("/fornecedores/excluir/<int:id>", methods=["POST"])
@login_required
def remover_fornecedor(id):
    excluir_fornecedor(id)
    return redirect("/fornecedores")


@app.route("/fornecedores/busca", methods=["POST"])
@login_required
def buscar_fornecedor_route():
    busca = request.form["busca"]
    if busca.isdigit():
        fornecedor = buscar_fornecedor(int(busca))
        lista = [fornecedor] if fornecedor else []
    else:
        lista = buscar_fornecedor_nome(busca)
    return render_template(
        "fornecedores.html",
        fornecedores=lista,
        total_fornecedores=len(lista),
        modo="criar"
    )


@app.route("/fornecedores/busca-cnpj", methods=["POST"])
@login_required
def buscar_fornecedor_cnpj_route():
    cnpj = request.form["cnpj"]
    lista = buscar_fornecedor_cnpj(cnpj)
    return render_template(
        "fornecedores.html",
        fornecedores=lista,
        total_fornecedores=len(lista),
        modo="criar"
    )


# ==================== VENDAS ====================

@app.route("/venda", methods=["POST"])
@login_required
def venda():
    id_cliente = request.form["cliente_id"]
    id_produto = request.form["produto_id"]
    quantidade = int(request.form["quantidade"])

    criar_tabela_vendas()
    lista = carregar_inscricoes()

    cliente = buscar_cliente_por_id(int(id_cliente))
    if not cliente:
        return render_home(lista, error="Cliente não encontrado!")

    sucesso, mensagem = registrar_venda(int(id_cliente), int(id_produto), quantidade)
    lista = carregar_inscricoes()

    if not sucesso:
        return render_home(lista, error=mensagem)

    return render_home(lista, success=mensagem)