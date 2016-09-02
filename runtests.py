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
