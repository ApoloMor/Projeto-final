import sqlite3
from database import conectar

# ----- INSCRIÇÕES  -----

def criar_tabela_inscricoes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_evento INTEGER NOT NULL
        )
""")

    conn.commit()
    conn.close()

def listar_inscricoes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inscricoes")

    inscricoes = cursor.fetchall()
    
    conn.close()

    return inscricoes

def buscar_inscricao(id): # Receber um id ↓ SELECT * FROM eventos WHERE id = ? ↓ fetchone()↓ return evento

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM inscricoes
                      WHERE id = ?""",(id,))
    
    inscricao = cursor.fetchone()

    conn.close()

    return inscricao

def inscrever_cliente_evento(id_cliente, id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inscricoes(id_cliente, id_evento)
        VALUES (?, ?)
    """, (id_cliente, id_evento))
 

    conn.commit()
    conn.close()

def excluir_inscricao(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM inscricoes WHERE id = ?",
        (id,) #isso vai baseado na linha em que o botão foi pressionado marcado vom seu respectivo id
    )

    conn.commit()
    conn.close()

def editar_inscricao(id, id_cliente, id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inscricoes 
        SET id_cliente = ?, id_evento = ?
        WHERE id = ?
    """, (id_cliente, id_evento, id))

    conn.commit()
    conn.close()

def contar_participantes(id_evento): #diz quantos inscritos em tal evento

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM inscricoes
        WHERE  id_evento = ?""", (id_evento,))

    quantidade = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return quantidade

def buscar_vagas_evento(id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vagas
        FROM eventos
        WHERE  id = ?""", (id_evento,))

    vagas = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return vagas

def vagas_disponiveis(id_evento):

    vagas_totais = buscar_vagas_evento(id_evento)
    inscritos = contar_participantes(id_evento)

    vagas_disponiveis = vagas_totais - inscritos

    return vagas_disponiveis

def evento_lotado(id_evento):

    return vagas_disponiveis(id_evento) <= 0