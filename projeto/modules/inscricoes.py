import sqlite3
from database import conectar
from modules.reutilizaveis import formatar_data

# ---- LOADER ----
def carregar_inscricoes():
    lista = listar_inscricoes()
    return adicionar_nomes(lista)

def adicionar_nomes(lista):

    inscricao_adicionada = []

    for inscricao in lista:
        inscricao = list(inscricao)

        nome_cliente = add_nome_cliente(inscricao[1])
        nome_evento = add_nome_evento(inscricao[2])
        data_evento = buscar_data_evento(inscricao[2])
        data_evento = formatar_data(data_evento)

        inscricao.append(nome_cliente)
        inscricao.append(nome_evento)
        inscricao.append(data_evento)
        inscricao_adicionada.append(inscricao)


    return inscricao_adicionada

def add_nome_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome
        FROM clientes
        WHERE id = ?
    """, (id_cliente,))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado[0] if resultado else None

def add_nome_evento(id_evento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome
        FROM eventos
        WHERE id = ?
    """, (id_evento,))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado[0] if resultado else None

def listar_inscricoes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inscricoes")

    inscricoes = cursor.fetchall()
    
    conn.close()

    return inscricoes

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

def ja_inscrito(id_cliente, id_evento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM inscricoes 
        WHERE id_cliente = ? AND id_evento = ?
    """, (id_cliente, id_evento))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0

def inscrever_cliente_evento(id_cliente, id_evento):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inscricoes(id_cliente, id_evento)
        VALUES (?, ?)
    """, (id_cliente, id_evento))
  
    conn.commit()
    conn.close()

def buscar_inscricao_por_id(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM inscricoes
                      WHERE id = ?""",(id,))
    
    inscricao = cursor.fetchone()

    conn.close()

    return inscricao

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

def excluir_inscricao(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM inscricoes WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

# ----- FILTROS -----

def filtrar_inscricao_id(busca):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * 
            FROM inscricoes
            WHERE id = ? """, (busca,)
)

    inscricao = cursor.fetchone()
  
    conn.close()

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

def filtrar_eventos_tipo_insc(tipo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.*
        FROM inscricoes i
        JOIN eventos e ON i.id_evento = e.id
        WHERE e.jogo = ?
    """, (tipo,))

    inscricoes = cursor.fetchall()

    conn.close()

    return inscricoes


# ----- RESUMO -----

def total_clientes_inscritos():#resumo

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT id_cliente)
        FROM inscricoes
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def total_eventos_com_vagas(): #resumo
    from modules.eventos import carregar_eventos

    eventos = carregar_eventos()

    total = 0

    for evento in eventos:

        if evento[6] == "Aberto" and vagas_disponiveis(evento[0]) > 0:
            total += 1

    return total

# ----- DEMAIS FUNÇÕES -----

def contar_inscricoes(id_evento): #Verifica para editar evento

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

def buscar_data_evento(id_evento): # Para o load
        
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT data
        FROM eventos
        WHERE  id = ?""", (id_evento,))

    data = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return data

def buscar_vagas_evento(id_evento): # Para o load

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

def vagas_disponiveis(id_evento): #multiuso

    vagas_totais = buscar_vagas_evento(id_evento)
    inscritos = contar_inscricoes(id_evento)

    vagas_disponiveis = vagas_totais - inscritos

    return vagas_disponiveis

def evento_lotado(id_evento):
    return vagas_disponiveis(id_evento) <= 0