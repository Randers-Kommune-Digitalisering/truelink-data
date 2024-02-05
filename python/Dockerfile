FROM python:alpine

WORKDIR /app

#RUN apt-get update -y
RUN apk add musl-dev
RUN apk add gcc
RUN apk add libpq-dev
RUN apk add mariadb-connector-c-dev

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-u", "app.py"]