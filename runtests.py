#!/usr/bin/env python
import os
import sys

if (
    "DATABASE_URL" not in os.environ or not
        os.environ["DATABASE_URL"].startswith("postgres://")):
    print("\n".join(
        l.strip() for l in
        """It seems you have not configured the path to your PGSQL database.")
        To do so, use the DATABASE_URL environment variable like this :

        DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME

        (where all optional parts can be omited to get their default value))
        """.splitlines()))
    sys.exit(1)

try:
    from django.conf import settings
    from django.test.utils import get_runner
    import dj_database_url

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={"default": dj_database_url.config(conn_max_age=600)},
        ROOT_URLCONF="runtests",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django_readonly_field.apps.ReadOnly",
            "tests.readonly_app",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
    )
    urlpatterns = []

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    msg = "To fix this error, run: pip install -r requirements_test.txt"
    raise ImportError(msg)


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
