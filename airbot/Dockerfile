FROM python:3.11-alpine

LABEL version=1.1.1

WORKDIR /app

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]