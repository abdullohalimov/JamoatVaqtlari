FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "sh", "entrypoint.sh" ]