cd ..
pyinstaller -F -n "Cadastro Melomano" --distpath bin/win --workpath bin/win --specpath win --icon=../cadastro_melomano/static/favicon.ico --add-data ../cadastro_melomano;cadastro_melomano app.py
