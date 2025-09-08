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

### Upgrading the database
After db upgrades, these commands need to run in the console
`./manage.py migrate`
`./manage.py update_index` // load wagtail users

## SPARQL endpoint

You need to set the environment variable "SPARQL_ENDPOINT", "SPARQL_PASSWORD", and "SPARQL_USERNAME".

## Datadog Voicebox authentication
environment variable VOICEBOX_BEARER_TOKEN needs to be set for voicebox functionality
