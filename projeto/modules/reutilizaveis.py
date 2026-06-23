from datetime import datetime
from flask import request
import math

def formatar_data(data):
    return datetime.strptime(
        data,
        "%Y-%m-%dT%H:%M"
    ).strftime("%d/%m/%Y %H:%M")

# ----- PAGINAS -----

def paginar(lista, por_pagina=10):

    pagina = request.args.get("pagina", 1, type=int)

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    total_paginas = math.ceil(len(lista) / por_pagina)

    return {
        "itens": lista[inicio:fim],
        "pagina": pagina,
        "total_paginas": total_paginas
    }