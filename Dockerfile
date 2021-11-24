FROM python:3.9

WORKDIR /var/www

RUN pip install flask==2.0.2 bs4==0.0.1 requests

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]