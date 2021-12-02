cd ..
python -m venv bin/win/venv
call bin/win/venv/Scripts/activate.bat
python -m pip install -r requirements.txt
pyinstaller -n "Cadastro Melomano" --paths bin/win/venv/Lib/site-packages --distpath bin/win/dist --workpath bin/win/build --specpath bin/win/spec --icon=../../../cadastro_melomano/static/favicon.ico --add-data ../../../cadastro_melomano;cadastro_melomano --add-data ../../../.env;. app.py