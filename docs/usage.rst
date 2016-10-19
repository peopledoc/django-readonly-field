========
Usage
========

In your ``settings.py``, use "django_readonly_field" as your database engine and set
``REAL_ENGINE`` for the engine that you will be using:

.. code-block:: python

    DATABASES["default"]["REAL_ENGINE"] = DATABASES["default"]["ENGINE"]
    DATABASES["default"]["ENGINE"] = "django_readonly_field"

Note: the django_readonly_field engine will not make your entire database readonly or what, but
we need an entrypoint to activate the field filtering, and as the database wrapper is rebuilded
frequently, we need to be there at that level to ensure that all connections will be modified.
We haven't (yet) found a better way to do this.

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
