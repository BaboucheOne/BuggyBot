FROM python:3.8-slim-buster

WORKDIR /buggybot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /buggybot

EXPOSE 27017

CMD ["python3", "main.py", "--env", "prod"]