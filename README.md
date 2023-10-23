# Quick start

1. pip install -r .\requirements.txt
2. python manage.py migrate
3. python manage.py runserver

## GDAL library

This is required if you're going to use any GEO features. If you do not
need any of these features comment out djgeojson and leaflet from `base.py`.

## Database

You can use SQLite or Postgres, Postgres is configured by default.

### Postgres

It needs to be PostgreSQL 12 or later. Make sure the database is running and
the "ch_lod" database is created.

## SPARQL endpoint

You need to set the environment variable "SPARQL_ENDPOINT", "SPARQL_PASSWORD", and "SPARQL_USERNAME".
