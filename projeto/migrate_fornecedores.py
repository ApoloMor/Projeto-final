import sqlite3
from database import conectar

# Deletar tabela antiga
conn = conectar()
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS fornecedores")
conn.commit()
conn.close()

# Recriar tabela com novos campos
from modules.fornecedores import criar_tabela_fornecedores, cadastrar_fornecedor

criar_tabela_fornecedores()

# Adicionar fornecedores de exemplo
fornecedores = [
    ("ElPepeProductions", "Pokémon TCG", "00.394.460/0058-87", "(67) 7890-3451", "ElPepe@gmail.com", "Alta"),
    ("PepsiCo", "Board Game", "31.565.104/0001-77", "0800 703 4444", "pepsico.corp@inpresspni.com.br", "Média"),
    ("TCG Direct", "Magic: The Gathering", "12.345.678/0001-99", "(11) 98765-4321", "contato@tcgdirect.com.br", "Alta"),
    ("Magical Cards", "Yu-Gi-Oh!", "45.678.901/0001-23", "(21) 99876-5432", "vendas@magicalcards.com.br", "Média"),
    ("Board Masters", "Board Game", "78.901.234/0001-56", "(85) 99654-3210", "contato@boardmasters.com.br", "Alta"),
    ("Pokemon Universe", "Pokémon TCG", "56.789.012/0001-34", "(31) 98765-4321", "info@pokemonuniverse.com.br", "Alta"),
    ("Card Traders", "Magic: The Gathering", "89.012.345/0001-67", "(47) 99765-4321", "support@cardtraders.com.br", "Média"),
    ("Gaming Hub", "Yu-Gi-Oh!", "34.567.890/0001-12", "(61) 98765-4321", "vendas@gaminghub.com.br", "Média"),
]

for nome, tipo, cnpj, telefone, email, margem in fornecedores:
    try:
        cadastrar_fornecedor(nome, tipo, cnpj, telefone, email, margem)
        print(f"✅ {nome} adicionado")
    except Exception as e:
        print(f"❌ Erro ao adicionar {nome}: {e}")

print("\n✅ Migração concluída!")
