import sqlite3
from database import conectar
from modules.produtos import saida_estoque, buscar_produtos

def criar_tabela_vendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id),
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )
    """)
    conn.commit()
    conn.close()

def registrar_venda(id_cliente, id_produto, quantidade):
    from datetime import datetime

    produto = buscar_produtos(id_produto)
    if not produto:
        return False, "Produto não encontrado"

    if produto[4] < quantidade:
        return False, f"Estoque insuficiente. Disponível: {produto[4]}"

    conn = conectar()
    cursor = conn.cursor()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute("""
        INSERT INTO vendas (id_cliente, id_produto, quantidade, data)
        VALUES (?, ?, ?, ?)
    """, (id_cliente, id_produto, quantidade, data))
    conn.commit()
    conn.close()

    saida_estoque(id_produto, quantidade)
    return True, "Venda registrada com sucesso"

def listar_vendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, c.nome, p.produto, v.quantidade, v.data
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN produtos p ON v.id_produto = p.id
        ORDER BY v.id DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado