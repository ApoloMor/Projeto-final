import sqlite3

conn = sqlite3.connect("database/gamestore.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM inscricoes")

conn.commit()
conn.close()

print("Inscrições apagadas com sucesso.")