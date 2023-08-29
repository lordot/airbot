FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY ../infra .

ENTRYPOINT ["sh", "entrypoint.sh"]