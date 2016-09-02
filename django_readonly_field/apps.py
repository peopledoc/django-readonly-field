from __future__ import unicode_literals

from django.apps import AppConfig


class ReadOnly(AppConfig):
    name = 'django_readonly_field'

    def ready(self):
        from django.db import connection
        connection.ops.compiler_module = "django_readonly_field.compiler"
