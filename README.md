# Nucleotide Query

## Introduction
This projects provides a web app for interactive regex matching against [SARS Cov Tor Nucleotide](https://www.ncbi.nlm.nih.gov/nuccore/30271926) as well as a CLI tool for matching [Homo sapiens chromosome 1, GRCh37.p13](https://www.ncbi.nlm.nih.gov/nuccore/NC_000001.10)

### Web app
#### 1. How to run  
You will need Docker cli tools including `docker-compose`.
> $DJANGO_ENV=production docker-compose up

This command will expose a web app at http://localhost.

#### 2. App Architecture  
The app uses `Django REST Framework` to build the API, with `Redis` as the caching backend. The app opt in the default use of `SQLite` with Django as the database.  Rather than using Django templates, the frontend was developed in `React` to enable rapid prototyping. An `NGINX` instance serves both the API and the built frontend application. All services and the building process are handled by `docker compose`.

#### 3. Model and View design  
There are three data models designed.

