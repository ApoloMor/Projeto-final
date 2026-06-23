import sqlite3
from database import conectar
from datetime import datetime
from modules.inscricoes import vagas_disponiveis
from modules.reutilizaveis import formatar_data

# ----- LOADER DA PAG  -----

def adicionar_status_eventos(lista):

    eventos_com_status = []

    for evento in lista:

        vagas = vagas_disponiveis(evento[0])

        status = obter_status_evento(
            evento[3],
            vagas
        )
        vagasOcupadas = evento[4] - vagas
        evento = list(evento)
        evento[3] = formatar_data(evento[3])
        evento.append(vagasOcupadas)
        evento.append(status)

        eventos_com_status.append(evento)

    return eventos_com_status

def carregar_eventos():
    lista = listar_eventos()
    return adicionar_status_eventos(lista)

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

    cursor.execute("""
        DELETE FROM inscricoes
        WHERE id_evento = ?
    """, (id,))

    cursor.execute("""
        DELETE FROM eventos
        WHERE id = ?
    """, (id,))

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

# ----- Vagas e Datas -----

def obter_status_evento(data_evento, vagas_disponiveis):

    data_evento = datetime.strptime( data_evento, "%Y-%m-%dT%H:%M" ) #tranforma de: "2026-06-13T18:00" para:  (2026, 6, 13, 18, 0)

    agora = datetime.now() #hora de agr no msm formato de cima

    if data_evento < agora:
        return "Encerrado"

    elif vagas_disponiveis <= 0:
        return "Lotado"

    else:
        return "Aberto"
    
def verificar_data(data):

    data_convertida = datetime.strptime( data, "%Y-%m-%dT%H:%M" )

    if data_convertida < datetime.now():
        return True

    return False


# ----- Fim Vagas e Data  -----



