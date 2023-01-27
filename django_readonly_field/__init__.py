import django

if django.VERSION[:2] < (3, 2):
    default_app_config = "django_readonly_field.apps.Readonly"
