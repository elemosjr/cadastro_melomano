#!/bin/sh
cd ..
pyinstaller -n "Cadastro Melomano" --distpath bin/linux --workpath bin/linux/build --specpath bin/linux/spec --icon="cadastro_melomano/static/favicon.ico" --add-data "../../../cadastro_melomano:cadastro_melomano" app.py
