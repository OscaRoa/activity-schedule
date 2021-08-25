FROM python:3.9-slim-buster

LABEL Author="Oscar Roa"

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

RUN apt-get -y update \
    && apt-get -y install apt-utils gcc python3-dev

COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY point.sh ./
RUN chmod +x ./point.sh

COPY . ./
RUN ls /usr/src/app
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
