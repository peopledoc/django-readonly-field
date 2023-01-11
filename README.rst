=============================
Django Readonly Field
=============================

.. image:: https://badge.fury.io/py/django-readonly-field.png
    :target: https://pypi.org/pypi/django-readonly-field

.. image:: https://travis-ci.org/peopledoc/django-readonly-field.png?branch=master
    :target: https://travis-ci.org/peopledoc/django-readonly-field

.. image:: https://img.shields.io/codecov/c/github/peopledoc/django-readonly-field/master.svg
    :target: https://codecov.io/github/peopledoc/django-readonly-field?branch=master

Make some Django model fields readonly. In other words, it lets you tell Django to
read some fields from your database, but never try to write those back. It can be
useful if your fields are populated by triggers or something.

Requirements
------------

+ **Postgresql only**
+ Django, tested from 2.2 to 4.1
+ With Python, tested from 3.7 to 3.11

Documentation
-------------

The full documentation is at https://django-readonly-field.readthedocs.org.

Quickstart
----------

Install Django Readonly Field::

    pip install django-readonly-field

In your ``settings.py`` :

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "django_readonly_field",
    ]

In the model where you want some fields to be read-only:

.. code-block:: python

    class Spaceship(models.Model):
        name = models.CharField(max_length=100)
        color = models.CharField(max_length=16)

        class ReadonlyMeta:
            readonly = ["color"]

That's it. Now, Django won't try to write the ``color`` field on the database.


Warning
-------

Django won't try to write those fields. Consequence is that your Database
**must** be ok with Django not writing those fields. They should either
be nullable or have a database default or be filled by a trigger, otherwise
you will get an ``IntegrityError``.

Don't forget that Django model field defaults won't become database defaults.
You might have to write an SQL migration for this.


Running Tests
--------------

You will need a usable Postgresql database in order to test the project.

::

    source <YOURVIRTUALENV>/bin/activate
    export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
    (myenv) $ pip install -r requirements.txt

Run tests for a specific version

::

    (myenv) $ pytest


Run tests for all versions (if tox is installed globally, you don't need a
virtual environment)

::

    $ tox


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
