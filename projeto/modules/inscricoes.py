import sqlite3
from database import conectar

# ----- CRUD INSCRIÇÕES  -----

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

def buscar_inscricao1(id): # Receber um id ↓ SELECT * FROM eventos WHERE id = ? ↓ fetchone()↓ return evento

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

def editar_inscricao(id, id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inscricoes 
        SET id_evento = ?
        WHERE id = ?
    """, (id_evento, id))

    conn.commit()
    conn.close()
  
# ----- FILTROS E BUSCAS INSCRIÇÕES  -----

def buscar_inscricao_id(busca):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * 
            FROM inscricoes
            WHERE id = ? """, (busca,)
)

    inscricao = cursor.fetchone()
  
    cursor.close()

    return inscricao

def filtrar_cliente_nome(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.*
        FROM inscricoes i
        JOIN clientes c ON i.id_cliente = c.id
        WHERE c.nome LIKE ?
    """, (f"%{nome}%",))

    inscricoes = cursor.fetchall()

    conn.close()

    return inscricoes

def filtrar_eventos_nome_insc(busca):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM eventos
        WHERE nome LIKE ?
    """, (f"%{busca}%",))

    evento = cursor.fetchone()

    if not evento:
        conn.close()
        return []

    cursor.execute("""
        SELECT *
        FROM inscricoes
        WHERE id_evento = ?
    """, (evento[0],))

    inscricoes = cursor.fetchall()

    conn.close()

    return inscricoes

# ----- sla  -----

def nome_cliente_id(id_cliente):
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * 
            FROM inscricoes
            WHERE id = ? """, (id_cliente,)
)

    inscricao = cursor.fetchone()
  
    cursor.close()

    return inscricao

# ----- DEMAIS FUNÇÕES -----

def contar_inscricoes(id_evento): #diz quantos inscritos em tal evento

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

def total_clientes_inscritos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT id_cliente)
        FROM inscricoes
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

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
    inscritos = contar_inscricoes(id_evento)

    vagas_disponiveis = vagas_totais - inscritos

    return vagas_disponiveis

def evento_lotado(id_evento):

    return vagas_disponiveis(id_evento) <= 0

def total_clientes_inscritos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM inscricoes
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def total_eventos_com_vagas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, vagas
        FROM eventos
    """)

    eventos = cursor.fetchall()

    total = 0

    for evento in eventos:

        id_evento = evento[0]
        vagas = evento[1]

        inscritos = contar_inscricoes(id_evento)

        if vagas > inscritos:
            total += 1

    conn.close()

    return total