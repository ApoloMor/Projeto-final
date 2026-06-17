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


