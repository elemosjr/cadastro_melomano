from flask import render_template, request, redirect, session, flash, url_for, send_file
from cadastro_melomano.app import app
from cadastro_melomano.utils import discogs, retorna_info_dados, InfoVinil, check_mesmo_tipo
import re
import os
import json
import datetime
import pandas as pd

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/editar", methods = ["POST", "GET"])
def editar():
    padrao_link = "(http://)?(https://)?(www.)?discogs.com.*"
    if "link" in request.form:
        link = request.form["link"]
        if re.fullmatch(padrao_link, link):
            discogs_info = discogs(link)
            if not check_mesmo_tipo(session, discogs_info):
                nome_classe = re.sub("Info", "", type(discogs_info).__name__)
                flash(f"Cadastro do tipo {nome_classe} difere dos dados da sessão.", "danger")
                return redirect(url_for("index"))
        else:
            flash("Link inválido.", "danger")
            return redirect(url_for("index"))
    else:
        discogs_info = retorna_info_dados(session, request)
    return render_template(
        "editar.html",
        discogs_info = discogs_info,
        vinil = isinstance(discogs_info, InfoVinil)
    )

@app.route("/visualizar", methods = ["GET", "POST"])
def visualizar():
    if "dados" not in session:
        if "gravadora" in request.form:
            session["dados"] = [
                [
                    "cód", "Artista", "Titulo", "Vinil", "Capa", "País",
                    "Gravadora", "Ano", "Descrição", "Estilo", "Preço"
                ]
            ]
        else:
            session["dados"] = [
                [
                    "cód", "Artista", "Titulo", "Vinil", "Capa",
                    "País", "Descrição", "Estilo", "Preço"
                ]
            ]

    if "artista" in request.form:
        if "gravadora" in request.form:
            dados_novos = [
                "",
                request.form["artista"],
                request.form["titulo"],
                "",
                "",
                request.form["pais"],
                request.form["gravadora"],
                request.form["ano"],
                re.sub("\r", "", re.sub("\n", " / ", request.form["desc"])),
                request.form["estilo"],
                ""
            ]
            session["dados"] += [dados_novos]
        else:
            dados_novos = [
                "",
                request.form["artista"],
                request.form["titulo"],
                "",
                "",
                request.form["pais"],
                re.sub("\r", "", re.sub("\n", " / ", request.form["desc"])),
                request.form["estilo"],
                ""
            ]
            session["dados"] += [dados_novos]
    if len(session["dados"][0]) == 11:
        tamanhos = [30, 140, 140, 40, 40, 60, 140, 40, 480, 160, 40]
    else:
        tamanhos = [30, 190, 200, 40, 40, 40, 480, 160, 40]
    return render_template(
        "visualizar.html",
        data = session["dados"],
        tamanhos = tamanhos
    )

@app.route("/limpar")
def limpar():
    if not session.get("dados") is None:
        session.pop("dados")
    return redirect(url_for("index"))

@app.route("/salvar")
def salvar():
    dados = session["dados"]
    dia = datetime.time().strftime('%d')
    cadastros = pd.DataFrame(dados[1:], columns = dados[0])
    path = os.path.join(app.root_path, "temp.xlsx")
    cadastros.to_excel(path, index = None, header = True)

    return send_file(path, as_attachment = True, download_name = f"{dia}.xlsx")

@app.route("/salvar_estado", methods = ["GET", "POST"])
def salvar_estado():
    dados = request.get_json()
    session["dados"] = dados["data"]
    return "ok"