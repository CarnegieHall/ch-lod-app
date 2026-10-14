from __future__ import absolute_import, unicode_literals

from .base import *
import os
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://data.carnegiehall.org']
USE_X_FORWARDED_HOST = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']
AZURE_CONNECTION_STRING = env['AZURE_CONNECTION_STRING']

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = False

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

_credential = DefaultAzureCredential()
_vault_client = SecretClient(
    vault_url=env['AZURE_VAULT_URL'],
    credential=_credential,
)
AZURE_CONNECTION_STRING = _vault_client.get_secret(
    env['AZURE_STORAGE_SECRET_NAME']
).value

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "connection_string": AZURE_CONNECTION_STRING,
            "azure_container": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass
