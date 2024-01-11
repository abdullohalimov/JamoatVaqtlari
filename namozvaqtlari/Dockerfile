FROM python:3.11-slim

RUN apt update
RUN apt install -y cron
RUN apt install -y p7zip-full

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "sh", "entrypoint.sh" ]