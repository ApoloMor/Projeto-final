import sqlite3
from database import conectar
from datetime import datetime

# ----- CRUD eventos -----

def criar_tabela_eventos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            jogo TEXT NOT NULL,
            data TEXT NOT NULL,
            vagas INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def cadastrar_evento(nome, jogo, data, vagas): #isso vem do formulario em html onde cada seção tem um name = 'argumento'

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO eventos(nome, jogo, data, vagas)
        VALUES (?, ?, ?, ?)
    """, (nome, jogo, data, vagas))

    conn.commit()
    conn.close()


def listar_eventos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM eventos") # seleciona tudo da tabela eventos

    eventos = cursor.fetchall()
    
    conn.close()

    return eventos # retorna tudo q selecionamos com o fetchall


def buscar_evento(id): # Receber um id ↓ SELECT * FROM eventos WHERE id = ? ↓ fetchone()↓ return evento

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM eventos
                      WHERE id = ?""",(id,))
    
    evento = cursor.fetchone()

    conn.close()

    return evento

def editar_evento(id, nome, jogo, data, vagas):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""UPDATE eventos
                      SET nome = ?, jogo = ?, data = ?, vagas = ?
                      WHERE id = ?""",
                      (nome, jogo, data, vagas, id)
                   )
    conn.commit()
    conn.close()
    

def excluir_evento(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM eventos WHERE id = ?",
        (id,) #isso vai baseado na linha em que o botão foi pressionado marcado vom seu respectivo id
    )

    conn.commit()
    conn.close()

# ----- FIM CRUD EVENTOS -----

# ----- Filtros  -----

def filtrar_eventos_id(busca):
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM eventos
                      WHERE id = ?""", (busca,))
    
    evento = cursor.fetchone()

    conn.close()

    return evento

def filtrar_eventos_nome(busca):
    
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM eventos
                      WHERE nome LIKE ?""", (f"%{busca}%",))
        
        evento = cursor.fetchall()

        conn.close()

        return evento


def filtrar_eventos_jogo(tipo):
         
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM eventos
                      WHERE jogo = ?""", (tipo,))
    
    evento = cursor.fetchall()

    conn.close()

    return evento

# ----- Fim Filtros  -----

# ----- Vagas  -----

def obter_status_evento(data_evento, vagas):

    data_evento = datetime.strptime(
        data_evento,
        "%Y-%m-%dT%H:%M" #tranforma de: "2026-06-13T18:00" para:  (2026, 6, 13, 18, 0)
    )

    agora = datetime.now() #hora de agr no msm formato de cima

    if int(vagas) <= 0:
        return "Lotado"

    elif data_evento < agora:
        return "Encerrado"

    else:
        return "Aberto"
    
# ----- Fim Vagas e EVENTOS  -----

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

def inscrever_cliente_evento(id_cliente, id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inscricoes(id_cliente, id_evento)
        VALUES (?, ?, ?, ?)
    """, (id_cliente, id_evento))
 

    conn.commit()
    conn.close()

def contar_participantes(id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM incricoes
        WHERE  id_evento = ?""", (id_evento))
 

    conn.commit()
    conn.close()


    