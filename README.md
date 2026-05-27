Projeto Final - Raciocinio Algoritmico
O projeto é um sistema desktop para uso interno de uma loja de board games e card games (Magic, Pokémon, Yu-Gi-Oh). O sistema permite que os funcionários cadastrem produtos, clientes, fornecedores e torneios, além de registrar as vendas e inscrições realizadas na loja. O sistema é desenvolvido em Python, com persistência de dados feita por meio da biblioteca pickle.

********** INTEGRANTES DO PROJETO: **********

BAIXEM O FLASK NO TERMINAL COM : pip install flask
EM CADA ARQUIVO(eu acho):
from flask import Flask, render_template, request, redirect
import pickle
import os

app = Flask(__name__)

PICKLE:
import pickle
nomes = ["Apolo", "João", "Maria"]
with open("database.pkl", "wb") as arquivo:
    pickle.dump(nomes, arquivo)

with open("database.pkl", "rb") as arquivo:
    dados = pickle.load(arquivo)

print(dados)
