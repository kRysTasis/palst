FROM continuumio/anaconda3:2020.02

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/palst/api

RUN apt-get update && apt-get install -y --no-install-recommends \
  net-tools \
  sudo \
  bzip2 \
  curl \
  gcc \
  git \
  python3-dev \
  vim \
  && \
  apt-get clean && \
  pip install --upgrade pip && \
  conda update -n base conda && \
  conda update --all && \
  conda clean --all -y && \
  conda install -c anaconda django && \
  conda install -c conda-forge django-filter && \
  conda install -c conda-forge djangorestframework && \
  conda install -c conda-forge djangorestframework-jwt && \
  conda install -c conda-forge django-cors-headers && \
  conda install -c anaconda python-memcached && \
  conda install -c anaconda psycopg2 && \
  conda install -c anaconda gunicorn && \
  conda install -c conda-forge dj-database-url && \
  conda install -c conda-forge django-environ && \
  pip install yahoo_finance_api2

ENV DJANGO_ENV develop
ADD . .
