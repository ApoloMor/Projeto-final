import sqlite3
from database import conectar


def criar_tabela_fornecedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def cadastrar_fornecedor(nome, cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fornecedores (nome, cnpj, telefone, email) VALUES (?, ?, ?, ?)",
        (nome, cnpj, telefone, email)
    )
    conn.commit()
    conn.close()


def listar_fornecedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    conn.close()
    return fornecedores


def buscar_fornecedor(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE id = ?", (id,))
    fornecedor = cursor.fetchone()
    conn.close()
    return fornecedor


def editar_fornecedor(id, nome, cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE fornecedores SET nome = ?, cnpj = ?, telefone = ?, email = ? WHERE id = ?",
        (nome, cnpj, telefone, email, id)
    )
    conn.commit()
    conn.close()


def excluir_fornecedor(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fornecedores WHERE id = ?", (id,))
    conn.commit()
    conn.close()