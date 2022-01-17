import os
import sys

import dj_database_url

if "DATABASE_URL" not in os.environ or \
        not os.environ["DATABASE_URL"].startswith("postgres://"):
    print("\n".join(
        "It seems you have not configured the path to your PGSQL database",
        "To do so, use the DATABASE_URL environment variable like this :",
        "",
        "    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME",
        "",
        "(where all optional parts can be omited to get their default value))"
    ))
    sys.exit(1)

DEBUG = True
USE_TZ = True
DATABASES = {"default": dj_database_url.config()}
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_readonly_field",
    "tests.readonly_app",
]
STATIC_URL = "/static/"
SITE_ID = 1
MIDDLEWARE_CLASSES = ()
LOGGING = {}
SECRET_KEY = "yay"
ROOT_URLCONF = "tests.readonly_app.views"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
