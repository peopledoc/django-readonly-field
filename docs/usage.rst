========
Usage
========

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
