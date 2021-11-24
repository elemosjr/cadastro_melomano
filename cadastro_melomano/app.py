from flask import Flask
import os


app = Flask(__name__)
app.config.from_pyfile("config.py")

from cadastro_melomano.views import *