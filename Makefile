.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with flake8
	flake8 --exclude="migrations,.tox,docs,build" .

test: ## run tests quickly with the default Python
	python runtests.py

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_readonly_field runtests.py

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django-readonly-field.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_readonly_field
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: clean ## package and upload a release
	python setup.py sdist bdist_wheel
	twine upload dist/*

sdist: clean ## package
	python setup.py sdist
	ls -l dist
