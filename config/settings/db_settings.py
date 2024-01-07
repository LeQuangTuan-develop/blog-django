from decouple import config, Csv
import os
from dj_database_url import parse as dburl
from pathlib import Path

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': config(
    'DATABASE_URL', default=default_dburl, cast=dburl),
}
