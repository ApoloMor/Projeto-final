#mudar de pickle pra SQL
import sqlite3

conexao = sqlite3.connect("gamestore.db")
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
    cursor.execute("""
                   INSERT INTO clientes
                    (nome, cpf, telefone, email) 
                   VALUES
                    (?, ?, ?, ?)
                   """, (nome, cpf, telefone, email))
    conexao.commit()

#get data -> usa-se select

def listar_clientes():
    cursor.execute("""SELECT * FROM clientes""")
    return cursor.fetchall()