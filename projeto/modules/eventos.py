import sqlite3
from database import conectar

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

def filtrar_id_eventos(id_busca):
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM eventos
                      WHERE id = ?""",(id_busca,))
    
    evento = cursor.fetchall()

    conn.close()

    return evento

def filtar_jogo_eventos():
    pass

def filtrar_nome_eventos():
    pass