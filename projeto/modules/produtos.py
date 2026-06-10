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
            estoque INTEGER NOT NULL,
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
        "DELETE FROM eventos WHERE id = ?",
        (id,) #isso vai baseado na linha em que o botão foi pressionado marcado vom seu respectivo id
    )

    conn.commit()
    conn.close()
