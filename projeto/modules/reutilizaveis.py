from datetime import datetime

def formatar_data(data):
    return datetime.strptime(
        data,
        "%Y-%m-%dT%H:%M"
    ).strftime("%d/%m/%Y %H:%M")
