from flask import flash, redirect, url_for, render_template
from bs4 import BeautifulSoup
import re
import requests


class InfoVinil:
    def __init__(self, artista, titulo, pais, label, year, tracks, tracks_len):
        self.artista = artista
        self.titulo = titulo
        self.pais = pais
        self.label = label
        self.year = year
        self.tracks = tracks
        self.tracks_len = tracks_len

class InfoCD:
    def __init__(self, artista, titulo, pais, info):
        self.artista = artista
        self.titulo = titulo
        self.pais = pais
        self.info = info


def get_master(soup):
    tracklist_id = "tracklist"
    track_name_class = "tracklist_track_title"
    main_div = soup.find_all("div", id = "page_content")[0]

    artista, titulo = [
            re.sub("\n+.*$", "", x.strip())
            for x in main_div.find("h1").text.split("–")
        ]

    track_list = []
    track_rows = soup.find("div", id = tracklist_id).find("table").find_all("tr")

    tracks = ""

    for row in track_rows:
        musica = row.find("td", class_ = re.compile(track_name_class)).text
        artist = row.find("td", class_ = re.compile("artist"))
        if artist:
            musica += artist.text
        track_list.append(musica.strip())

    tracks = "\n".join(track_list)

    info_content = list(map(lambda x: x.text, soup.find("div", class_ = "profile").find_all("div", class_ = "content")))
    info_head = list(map(lambda x: x.text, soup.find("div", class_ = "profile").find_all("div", class_ = "head")))

    year = ""

    year_head = "Year:"
    if year_head in info_head:
        year_idx = info_head.index(year_head)
        year = re.search("\\d{4}", info_content[year_idx]).group()
    
    return InfoVinil(artista, titulo, "", "", year, tracks, len(track_list))


def get_release(soup):
    tracklist_id = "release-tracklist"
    track_name_class = "^trackTitle*"
    main_div = soup.find_all("div", class_ = re.compile("main_*"))[0]
    info_rows = main_div.find_all("tr")
    info_headers = list(map(lambda x: x.text, main_div.find_all("th")))

    artista, titulo = [
            re.sub("\n+.*$", "", x.strip())
            for x in main_div.find("h1").text.split("–")
        ]

    country = ""
    country_head = "Country:"
    if country_head in info_headers:
        country_idx = info_headers.index(country_head)
        country = re.sub(f"^{country_head}", "", info_rows[country_idx].text)

    label = ""
    label_head = "Label:"
    if label_head in info_headers:
        label_idx = info_headers.index(label_head)
        label = re.sub(f"^{label_head}", "", info_rows[label_idx].text)

    year = ""

    year_head = "Released:"
    if year_head in info_headers:
        year_idx = info_headers.index(year_head)
        year = re.search("\\d{4}", info_rows[year_idx].text).group()

    track_list = []
    track_rows = soup.find("section", id = tracklist_id).find("table").find_all("tr")

    tracks = ""

    for row in track_rows:
        musica = row.find("td", class_ = re.compile(track_name_class)).text
        artist = row.find("td", class_ = re.compile("artist"))
        if artist:
            musica += artist.text
        track_list.append(musica)

    tracks = "\n".join(track_list)

    tracks_len = len(track_list)

    formato = ""

    format_head = "Format:"
    if format_head in info_headers:
        format_idx = info_headers.index(format_head)
        formato = re.sub(f"^{format_head}", "", info_rows[format_idx].text)

    if "CD" in formato:
        return None
    else:
        return InfoVinil(artista, titulo, country, label, year, tracks, tracks_len)


def discogs(link):
    master_re = "(http://)?(https://)?(www.)?discogs.com/master/.*"
    release_re = "(https://)?(http://)?(www.)?discogs.com/release/.*"

    master = re.fullmatch(master_re, link)
    release = re.fullmatch(release_re, link)

    pagina = requests.get(link)
    soup = BeautifulSoup(pagina.content, "html.parser")

    if master:
        return get_master(soup)
    elif release:
        return get_release(soup)
    else:
        return InfoVinil(*[""] * 7)

