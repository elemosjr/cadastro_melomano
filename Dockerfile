FROM python:3.9

WORKDIR /var/www

COPY cadastro_melomano /var/www/cadastro_melomano/
COPY * /var/www/

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]