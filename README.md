# ch-lod-app

Django/Wagtail site for [data.carnegiehall.org](https://data.carnegiehall.org).

## Local development setup

### Prerequisites

- Python 3.12
- Git

### 1. Clone and create a virtual environment

```
cd ch-lod-app
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Enter the env any time later with `.venv\Scripts\activate`

### 2. Create a `.env` file

Create a `.env` file in the project root with at minimum the following. They can be gotten from the Heroku app settings under config vars.

```
SPARQL_BASEURL=<stardog cloud base URL>
SPARQL_DB_NAME=<database name>
SPARQL_USERNAME=<username>
SPARQL_PASSWORD=<password>
VOICEBOX_BEARER_TOKEN=<token>
```

The `.env` file is in `.gitignore` and should never be committed.

### 3. Migrate and create a superuser

```powershell
python manage.py migrate --settings=ch_lod.settings.dev
python manage.py createsuperuser --settings=ch_lod.settings.dev
```

### 4. Run the dev server

```powershell
python manage.py runserver --settings=ch_lod.settings.dev
```

The site will be at `http://127.0.0.1:8000/` and the Wagtail admin at `http://127.0.0.1:8000/wagtail-admin/`.

## Database

`dev.py` uses SQLite by default, no db setup needed. It's only needed for wagtail posts, so probably leave it as sqlite. If you really want to use PostgreSQL locally instead, swap the `DATABASES` config in `dev.py` and make sure you have a `ch_lod` database created (PostgreSQL 12+).

After switching databases or deleting the SQLite file, re-run migrate and createsuperuser.

## GDAL / geo features

The geo features (`djgeojson`, `leaflet`) require GDAL, which is provided by [OSGeo4W](https://trac.osgeo.org/osgeo4w/) on Windows. These are disabled in `dev.py` by default.

If you need geo features locally:

1. Install OSGeo4W to `C:\OSGeo4W`
2. In `dev.py`, uncomment the OSGeo4W environment block
3. Remove `'djgeojson'` and `'leaflet'` from `_REMOVE_APPS`

## Search index

After loading content or switching databases:

```powershell
python manage.py update_index --settings=ch_lod.settings.dev
```

## Production

Production settings are in `ch_lod/settings/production.py` and are configured via Heroku environment variables.