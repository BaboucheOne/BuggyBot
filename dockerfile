FROM python:3.10-slim-buster

CMD ["pip", "install", "--upgrade", "pip"]

WORKDIR /buggybot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /buggybot

EXPOSE 27017

CMD ["python3", "main.py", "--env", "prod"]
