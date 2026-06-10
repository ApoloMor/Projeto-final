import os
import sqlite3

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA_ATUAL, "..", "database", "gamestore.db")

conexao = sqlite3.connect(CAMINHO_BANCO)

cursor = conexao.cursor()

#mandar comandos para o banco
def criar_tabela():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, 
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )""")
    conexao.commit() #salvar as alteracoes

#cursor.execute("""sql""", valores) -> 1. pega os sql com ? ->entrega pro banco; 2. pega os valores -> entrega pro banco separadamente
#o banco que junta as duas coisas, python vai so entregar
def inserir_cliente(nome, cpf, telefone, email):
    try:    
        cursor.execute("""
                       INSERT INTO clientes
                        (nome, cpf, telefone, email) 
                       VALUES
                        (?, ?, ?, ?)
                       """, (nome, cpf, telefone, email))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False

#get data -> usa-se select

def listar_clientes():
    cursor.execute("""SELECT * FROM clientes""")
    return cursor.fetchall()

def editar_cliente(id, nome, cpf, telefone, email):
    try:
        cursor.execute("""UPDATE clientes SET nome = ?, cpf = ?, telefone = ?, email = ? WHERE id = ?""", (nome, cpf, telefone, email, id))
        if cursor.rowcount == 0:
            return False
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def buscar_cliente(cpf):
    cursor.execute("""SELECT * FROM clientes WHERE cpf = ?""", (cpf,))
    return cursor.fetchone()

def buscar_cliente_nome(nome):
    cursor.execute("""SELECT * FROM clientes WHERE nome LIKE ?""", (f"%{nome}%",))
    return cursor.fetchall()

def remover_cliente(id):
    cursor.execute("""DELETE FROM clientes WHERE id = ? """, (id,))
    if cursor.rowcount == 0:
        return False
    conexao.commit()
    return True
