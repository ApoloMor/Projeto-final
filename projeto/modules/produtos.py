import sqlite3
from database import conectar


def criar_tabela_produtos():
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            tipo TEXT NOT NULL,
            preco INTEGER NOT NULL,
            estoque INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def cadastrar_produtos(produto, tipo, preco, estoque):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produtos(produto, tipo, preco, estoque)
        VALUES (?, ?, ?, ?)
    """, (produto, tipo, preco, estoque))

    conn.commit()
    conn.close()


def excluir_produtos(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,) #isso vai baseado na linha em que o botão foi pressionado marcado vom seu respectivo id
    )

    conn.commit()
    conn.close()

def listar_produtos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos") # seleciona tudo da tabela 

    produtos = cursor.fetchall()
    
    conn.close()

    return produtos # retorna tudo q selecionamos com o fetchall

def buscar_produtos(id): 

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM produtos
                      WHERE id = ?""",(id,))
    
    produto = cursor.fetchone()

    conn.close()

    return produto

def editar_produtos(id, produto, tipo, preco, estoque):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""UPDATE produtos
                      SET produto = ?, tipo = ?, preco = ?, estoque = ?
                      WHERE id = ?""",
                      (produto, tipo, preco, estoque, id)
                   )
    conn.commit()
    conn.close()


def buscar_produtos_nome(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE produto LIKE ?", (f"%{nome}%",))
    produtos = cursor.fetchall()

    conn.close()
    return produtos


def buscar_produtos_por_tipo(tipo):
    tipos_map = {
        "pokemon": "Pokémon TCG",
        "magic": "Magic: The Gathering",
        "yugioh": "Yu-Gi-Oh!",
        "board": "Board Game"
    }

    tipo_real = tipos_map.get(tipo, tipo)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE tipo = ?", (tipo_real,))
    produtos = cursor.fetchall()

    conn.close()
    return produtos


def entrada_estoque(id, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (quantidade, id))
    conn.commit()
    conn.close()
    registrar_movimentacao(id, "Entrada", quantidade)  


def saida_estoque(id, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (quantidade, id))
    conn.commit()
    conn.close()
    registrar_movimentacao(id, "Saída", quantidade)  

def criar_tabela_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            tipo TEXT NOT NULL,         -- 'Entrada' ou 'Saída'
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )
    """)
    conn.commit()
    conn.close()


def registrar_movimentacao(id_produto, tipo, quantidade):
    from datetime import datetime
    conn = conectar()
    cursor = conn.cursor()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute("""
        INSERT INTO movimentacoes (id_produto, tipo, quantidade, data)
        VALUES (?, ?, ?, ?)
    """, (id_produto, tipo, quantidade, data))
    conn.commit()
    conn.close()


def listar_movimentacoes(id_produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo, quantidade, data
        FROM movimentacoes
        WHERE id_produto = ?
        ORDER BY id DESC
        LIMIT 20
    """, (id_produto,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def listar_todas_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.data, p.produto, m.tipo, m.quantidade
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id
        ORDER BY m.id DESC
        LIMIT 50
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado