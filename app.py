from flask import Flask, render_template, request, redirect
import pickle
import os

app = Flask(__name__)