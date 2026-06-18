import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_BANCO = os.path.join(
    BASE_DIR,
    "database",
    "gamestore.db"
)

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


