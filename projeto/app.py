from flask import Flask

app = Flask(__name__)

from modules.produtos import *
from modules.clientes import *
from modules.fornecedores import *
from modules.eventos import *
from modules.vendas import *

if __name__ == "__main__":
    app.run(debug=True)