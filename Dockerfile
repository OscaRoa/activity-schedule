FROM python:3.9-alpine3.13

LABEL Author="Oscar Roa"

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
EXPOSE 8000

COPY Pipfile Pipfile.lock /app/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev linux-headers && \
    pipenv install --system --deploy && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol

# ENV PATH="/py/bin:$PATH"
# ENV WORKON_HOME="/py/bin"

COPY ./project /app

COPY ./scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:$PATH"

USER app

CMD ["run.sh"]

# COPY entrypoint.sh ./
# RUN chmod +x ./entrypoint.sh

# COPY . ./
# RUN ls /usr/src/app
# # ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
