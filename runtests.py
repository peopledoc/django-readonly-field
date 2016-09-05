#!/usr/bin/env python
import sys
import os

try:
    from django import setup
except ImportError:
    import traceback
    traceback.print_exc()
    msg = "To fix this error, run: pip install -r requirements_test.txt"
    raise ImportError(msg)

from django.test.utils import get_runner
from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "tests.readonly_project.settings"
setup()


def run_tests(*test_args):
    from django.core.management import execute_from_command_line
    execute_from_command_line(["", "test", ] + sys.argv[1:])


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
