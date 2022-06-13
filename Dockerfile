FROM python:3.9.6-alpine

ADD . /api
WORKDIR /api

# set environment variables
ENV DATABASE_ENGINE django.db.backends.postgresql_psycopg2
ENV DATABASE_NAME sek9
ENV DATABASE_USER_NAME postgres
ENV DATABASE_PASSWORD postgres123qwe!#QWE
ENV DATABASE_HOST sek9-prod.ctvmnntxrnbe.eu-west-3.rds.amazonaws.com
ENV DATABASE_PORT 5432
ENV AWS_ACCESS_KEY_ID TEST
ENV AWS_SECRET_ACCESS_KEY TEST_KEY
ENV AWS_STORAGE_BUCKET_NAME sek9
ENV SITE_URL https://app.sek9.com
ENV EMAIL_HOST = 'smtp.gmail.com'
ENV EMAIL_HOST_USER admin@sek9.com
ENV EMAIL_HOST_PASSWORD 123qweasd
ENV EMAIL_PAGE_DOMAIN https://app.sek9.com/
ENV REDIS_URL redis://:LESaliFR2020@172.20.0.10:6379/4
ENV PORT 8000
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add --no-cache --virtual .build-deps
RUN apk add --no-cache \
    bash \
    build-base \
    cairo \
    cairo-dev \
    cargo \
    freetype-dev \
    fribidi-dev \
    gcc \
    gdk-pixbuf-dev \
    gettext \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    libc-dev \
    libffi-dev \
    openjpeg-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    make \
    musl-dev \
    openssl-dev \
    pango-dev \
    poppler-utils \
    postgresql-client \
    postgresql-dev \
    python3-dev \
    py-cffi \
    py-pip \
    rust \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    zlib
RUN apk add postgresql
RUN pip install --upgrade pip
RUN pip install psycopg2 cython
RUN apk del .build-deps

RUN mkdir -p /root/.aws/
COPY ./aws/config /root/.aws/config
COPY ./aws/credentials /root/.aws/credentials

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "entrypoint.sh"]
