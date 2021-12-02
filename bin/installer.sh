#!/bin/sh
cd ..
python -m venv bin/linux/venv
source bin/linux/venv/bin/activate
python -m pip install -r requirements.txt
pyinstaller -n "Cadastro Melomano" --paths bin/linux/venv/lib/python*/site-packages --distpath bin/linux/dist --workpath bin/linux/build --specpath bin/linux/spec --icon="cadastro_melomano/static/favicon.ico" --add-data "../../../cadastro_melomano:cadastro_melomano" --add-data "../../../.env:." app.py