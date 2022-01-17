from django.apps import AppConfig


class Readonly(AppConfig):
    name = 'django_readonly_field'

    def ready(self):
        from django.db import connections
        from django.db import utils

        readonly_compiler_module = "django_readonly_field.compiler"

        # Change the current values (this is mostly important for the tests)
        for c in connections:
            connections[c].ops.compiler_module = readonly_compiler_module

        original_load_backend = utils.load_backend

        def custom_load_backend(*args, **kwargs):
            backend = original_load_backend(*args, **kwargs)

            class ReadOnlyBackend(object):
                @staticmethod
                def DatabaseWrapper(*args2, **kwargs2):
                    connection = backend.DatabaseWrapper(*args2, **kwargs2)
                    connection.ops.compiler_module = readonly_compiler_module
                    return connection

            return ReadOnlyBackend

        # Make sure all future values will be changed too
        # (this is mostly important for the real life)
        utils.load_backend = custom_load_backend
