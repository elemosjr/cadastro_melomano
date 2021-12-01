from __future__ import annotations
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()


DISCOGS_API_TOKEN = os.environ.get("DISCOGS_API_TOKEN")
RELEASE_URL = "https://api.discogs.com/releases/{}?token={}"
MASTER_URL = "https://api.discogs.com/masters/{}?token={}"

class InfoVinil:
    def __init__(self, artista, titulo, pais, selo, ano, faixas, tracks_len):
        self.artista = artista
        self.titulo = titulo
        self.pais = pais
        self.selo = selo
        self.ano = ano
        self.faixas = faixas
        self.tracks_len = tracks_len

    def __str__(self):
        return f"""Artista: {self.artista}\nTítulo: {self.titulo}\n
                   País: {self.pais}\nSelo: {self.selo}\n
                   Ano: {self.ano}\nFaixas: {self.faixas}"""

class InfoCD:
    def __init__(self, artista, titulo, pais, info, tracks_len):
        self.artista = artista
        self.titulo = titulo
        self.pais = pais
        self.info = info
        self.tracks_len = tracks_len


    def __str__(self):
        return f"""Artista: {self.artista}\nTítulo: {self.titulo}\n
                   País: {self.pais}\Informações: {self.info}"""


def formata_artista(artistas):
    aux = []
    for artista in artistas:
        nome = re.sub("( \([0-9]+\)$)?(\*)?", "", artista["name"])
        aux.append(nome)
    return ", ".join(aux)

def formata_selo(selos):
    aux = []
    for selo in selos:
        aux.append(f"{selo['name']} - {selo['catno']}")
    return ", ".join(aux)

def lista_faixas(faixas):
    aux = []
    for faixa in faixas:
        try:
            string = f"{faixa['title']} ({formata_artista(faixa['artists'])})"
        except KeyError:
            string = faixa["title"]
        try:
            sub_tracks = " / ".join(lista_faixas(faixa["sub_tracks"]))
            string += f" ({sub_tracks})"
        except:
            pass
        string = re.sub("^[ \t]+", "", string)
        aux.append(string)
    return aux

def formata_formatos(formatos):
    aux = []
    for formato in formatos:
        aux.append(formato["name"])
    return ", ".join(aux)

def busca(body, item):
    try:
        return body[item]
    except:
        return ""

def get_master(master_id):
    master_r = requests.get(MASTER_URL.format(master_id, DISCOGS_API_TOKEN))

    if master_r.status_code == 200:
        body = master_r.json()

        artista = formata_artista(busca(body, "artists"))
        titulo = busca(body, "title")
        ano = busca(body, "year")
        if ano:
            titulo = f"{titulo} ({ano})"
        tracklist = lista_faixas(busca(body, "tracklist"))
        tracks_len = len(tracklist)
        faixas = "\n".join(tracklist)

        if "CD" in formata_formatos(busca(body, "formats")):
            info = f"Músicas: {faixas}"
            if ano:
                info += f" ({ano})"
            return InfoCD(artista, titulo, "", info, tracks_len)
        else:
            return InfoVinil(artista, titulo, "", "", ano, f"Músicas: {faixas}", tracks_len)
    else:
        return False

def get_release(release_id):
    release_r = requests.get(RELEASE_URL.format(release_id, DISCOGS_API_TOKEN))

    if release_r.status_code == 200:
        body = release_r.json()

        try:
            master_url = body["master_url"]
            master_r = requests.get(f"{master_url}?token={DISCOGS_API_TOKEN}")

            if master_r.status_code == 200:
                ano_master = busca(master_r.json(), "year")
        except KeyError:
            pass

        artista = formata_artista(busca(body, "artists"))
        titulo = busca(body, "title")
        ano = busca(body, "year")

        try:
            titulo = f"{titulo} ({ano_master})"
        except:
            titulo = f"{titulo} ({ano})"

        pais = busca(body, "country")
        selo = formata_selo(busca(body, "labels"))
        tracklist = lista_faixas(busca(body, "tracklist"))
        tracks_len = len(tracklist)
        faixas = "\n".join(tracklist)

        if "CD" in formata_formatos(busca(body, "formats")):
            info = f"Músicas: {faixas} - {selo}"
            if ano:
                info += f" ({ano})"
            return InfoCD(artista, titulo, pais, info, tracks_len)
        else:
            return InfoVinil(artista, titulo, pais, selo, ano, f"Músicas: {faixas}", tracks_len)
    else:
        return False

def discogs(link):
    master_re = "(http://)?(https://)?(www.)?discogs.com/master/[0-9]+.*"
    release_re = "(https://)?(http://)?(www.)?discogs.com/release/[0-9]+.*"

    if re.fullmatch(master_re, link):
        master_id = re.search("(\\d+)", link).group(1)
        return get_master(master_id)
    elif re.fullmatch(release_re, link):
        release_id = re.search("(\\d+)", link).group(1)
        return get_release(release_id)
    else:
        return False

def check_mesmo_tipo(session, obj):
    if session.get("dados"):
        if "Gravadora" in session["dados"][0]:
            if obj.selo:
                return True
        else:
            if not "selo" in dir(obj):
                return True
        return False
    return True

def retorna_info_dados(session, request):
    """Retorna Informações objeto de informações vazio de acordo com os dados da sessão
    """
    if session.get("dados"):
        if "Gravadora" not in session["dados"][0]:
            return InfoCD(*[""] * 5)
    return InfoVinil(*[""] * 7)