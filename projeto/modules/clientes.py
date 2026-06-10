import sqlite3
from database import conectar

#mandar comandos para o banco
def criar_tabela_clientes():
    conexao = conectar()          
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, 
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )""")
    conexao.commit() #salvar as alteracoes
    conexao.close()

#cursor.execute("""sql""", valores) -> 1. pega os sql com ? ->entrega pro banco; 2. pega os valores -> entrega pro banco separadamente
#o banco que junta as duas coisas, python vai so entregar
def cadastrar_cliente(nome, cpf, telefone, email):
    conexao = conectar()         
    cursor = conexao.cursor()
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
    finally:
        conexao.close()

#get data -> usa-se select

def listar_clientes():
    conexao = conectar()         
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM clientes""")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def editar_cliente(id, nome, cpf, telefone, email):
    conexao = conectar()        
    cursor = conexao.cursor()
    try:
        cursor.execute("""UPDATE clientes SET nome = ?, cpf = ?, telefone = ?, email = ? WHERE id = ?""", (nome, cpf, telefone, email, id))
        if cursor.rowcount == 0:
            return False
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexao.close()

def buscar_cliente_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM clientes WHERE id = ?""", (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def buscar_cliente(cpf):
    conexao = conectar()         
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM clientes WHERE cpf = ?""", (cpf,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def buscar_cliente_nome(nome):
    conexao = conectar()        
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM clientes WHERE nome LIKE ?""", (f"%{nome}%",))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def excluir_cliente(id):
    conexao = conectar()       
    cursor = conexao.cursor()
    try:    
        cursor.execute("""DELETE FROM clientes WHERE id = ? """, (id,))
        if cursor.rowcount == 0:
            return False
        conexao.commit()
        return True
    finally:
        conexao.close()