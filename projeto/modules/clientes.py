"""
modulo de clientes: cadastrar, listar, editar e remover os clientes da loja
id, nome, cpf, telefone, email

#lista com varios dicionarios, cada dicionarios tem o cliente com suas informacoes 
"""

import pickle
import os
ARQUIVO = "clientes.pkl"

print("=-="*10, "Menu", "=-="*10)

print("1. Cadastrar\n2. Listar\n3. Editar\n4. Remover\n5. Sair")

#ler os clientes salvos no arquivo
def carregar():
    if not os.path.exists(ARQUIVO): #se nn existe eh pra devolver a lista vazia
        return []
    else:
        with open(ARQUIVO, "rb") as f: #with open eh uma forma boa pra abrir arquivos
            return pickle.load(f)

#gravar a lista no arquivo clientes.pkl        
def salvar(lista):
    with open(ARQUIVO, "wb") as f:
        pickle.dump(lista, f) #dump grava dentro do arquivo

"""
- inputs ver oq fazer com isso dps e aprimorar
lista = carregar()
novoCliente = {}
novoCliente["id"] = len(lista) + 1 # +1 pq esse cliente eh o proximo, entt +1
novoCliente["nome"] = input("Nome completo do cliente: ")
novoCliente["cpf"] = input("CPF: ")
novoCliente["telefone"] = input("Telefone: " )
novoCliente["email"] = input("Insira o email: ")
lista.append(novoCliente)
salvar(lista)
"""

def validarCPF(cpf): # validação: verifica se o CPF já existe
    lista = carregar(lista)
    for cliente in lista:
        if cliente["cpf"] == cpf:
            print("CPF ja existe")
            return False
        
# id, nome, cpf, telefone, email
def cadastrar(nome, cpf, telefone, email):
    novoCliente = {}
    lista = carregar()
    #gerar id
    id = len(lista) 
    #monta dicionário, append e dps salva
    novoCliente["id"] = id
    novoCliente["nome"] = nome
    novoCliente["cpf"] = cpf
    novoCliente["telefone"] = telefone
    novoCliente["email"] = email
    validar = validarCPF(cpf)
    if validar == False:
        print("Este CPF ja existe")
        return False
    lista.append(novoCliente)
    salvar(lista)
    return True   #se deu certo