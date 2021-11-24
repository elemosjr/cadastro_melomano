from flask import render_template, request, redirect, session, flash, url_for
from cadastro_melomano.app import app
from cadastro_melomano.utils import discogs, InfoVinil

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/editar", methods = ["POST", "GET"])
def editar():
    if "link" not in request.form:
        discogs_info = InfoVinil(*[""] * 7)
    else:
        link = request.form["link"]
        discogs_info = discogs(link)
    return render_template(
        "editar.html",
        discogs_info = discogs_info,
        vinil = isinstance(discogs_info, InfoVinil)
    )

@app.route("/visualizar")
def visualizar():
    return render_template("index.html")