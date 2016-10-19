from django.core.exceptions import ImproperlyConfigured
from django.db.utils import load_backend


def DatabaseWrapper(settings_dict, *args, **kwargs):
    try:
        real_engine = settings_dict["REAL_ENGINE"]
    except KeyError:
        raise ImproperlyConfigured(
            "When using readonly DB ENGINE, you must "
            "provide a REAL_ENGINE key")

    engine = load_backend(real_engine).DatabaseWrapper(
        settings_dict, *args, **kwargs)
    engine.ops.compiler_module = "django_readonly_field.compiler"
    return engine
