FROM python:3.10.6-slim-buster

#ENV PYTHONPATH "${PYTHONPATH}:/"
#ENV PORT=8000
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install netcat gcc postgresql && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
