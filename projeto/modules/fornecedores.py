import sqlite3
from database import conectar


def criar_tabela_fornecedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            margem_lucro TEXT NOT NULL
        )
    """)
    
    # Tenta adicionar colunas se não existirem (para migração)
    try:
        cursor.execute("ALTER TABLE fornecedores ADD COLUMN tipo TEXT")
    except:
        pass
    
    try:
        cursor.execute("ALTER TABLE fornecedores ADD COLUMN margem_lucro TEXT")
    except:
        pass
    
    conn.commit()
    conn.close()


def cadastrar_fornecedor(nome, tipo, cnpj, telefone, email, margem_lucro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fornecedores (nome, tipo, cnpj, telefone, email, margem_lucro) VALUES (?, ?, ?, ?, ?, ?)",
        (nome, tipo, cnpj, telefone, email, margem_lucro)
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


def editar_fornecedor(id, nome, tipo, cnpj, telefone, email, margem_lucro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE fornecedores SET nome = ?, tipo = ?, cnpj = ?, telefone = ?, email = ?, margem_lucro = ? WHERE id = ?",
        (nome, tipo, cnpj, telefone, email, margem_lucro, id)
    )
    conn.commit()
    conn.close()


def excluir_fornecedor(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fornecedores WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def buscar_fornecedor_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE nome LIKE ?", (f"%{nome}%",))
    fornecedores = cursor.fetchall()
    conn.close()
    return fornecedores


def buscar_fornecedor_cnpj(cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE cnpj LIKE ?", (f"%{cnpj}%",))
    fornecedores = cursor.fetchall()
    conn.close()
    return fornecedores