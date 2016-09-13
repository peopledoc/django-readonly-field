#!/usr/bin/env python
import sys
import os
import contextlib


@contextlib.contextmanager
def cover():
    do_coverage = "COVERAGE" in os.environ

    if do_coverage:
        import coverage
        cov = coverage.Coverage(source=["django_readonly_field"])
        cov.start()
        print("Coverage will be generated")

    try:
        yield
    finally:
        if do_coverage:
            cov.stop()
            cov.save()


def run_tests(*test_args):

    with cover():
        try:
            from django import setup
        except ImportError:
            import traceback
            traceback.print_exc()
            msg = ("To fix this error, run: "
                   "pip install -r requirements_test.txt")
            raise ImportError(msg)

        module = "tests.readonly_project.settings"
        os.environ["DJANGO_SETTINGS_MODULE"] = module
        setup()

        from django.core.management import execute_from_command_line
        execute_from_command_line(["", "test", ] + sys.argv[1:])


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
