from .base import *

import os

# ---- Windows GDAL setup (uncomment if you need geo features locally) ----
# Requires OSGeo4W installed to C:\OSGeo4W
# Also remove 'djgeojson' and 'leaflet' from _REMOVE_APPS below
#
# if os.name == 'nt':
#     OSGEO4W = r"C:\OSGeo4W"
#     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
#     os.environ['OSGEO4W_ROOT'] = OSGEO4W
#     os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
#     os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#     os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

# ---- Django / Wagtail fixes ----
WAGTAILADMIN_BASE_URL = "/"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# ---- Dev basics ----
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1wkgdvpvsoe#$mhru0i6@482_te#!6w_4+3-r8!ojkav24-w8j'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# ---- Database ----
# SQLite for local dev - no Postgres setup needed.
# Switch to Postgres if you need production-like data locally,
# it's only used for the wagtail blog posts though so not needed for dev most likely.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ch_lod',
#     }
# }

# ---- Remove apps that need Postgres or GDAL for SQLite local dev ----
# If you enable geo features above, remove 'djgeojson' and 'leaflet' from this list.
_REMOVE_APPS = [
    'wagtail.search.backends.database',  # not a real Django app, only in INSTALLED_APPS as legacy
    'djgeojson',                          # needs GDAL
    'leaflet',                            # needs GDAL
]
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in _REMOVE_APPS]

# Clear the postgres search backend config from base.py.
# Wagtail falls back to its built-in default which works with SQLite.
WAGTAILSEARCH_BACKENDS = {}

# After switching databases or creating a clean slate, run:
#   python manage.py migrate --settings=ch_lod.settings.dev
#   python manage.py createsuperuser --settings=ch_lod.settings.dev

try:
    from .local import *
except ImportError:
    pass