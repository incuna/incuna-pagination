SHELL := /bin/bash
VERBOSITY := 1

help:
	@echo "usage:"
	@echo "	make release -- release to Incuna's pypi"
	@echo "	make test -- run the tests, including flake8 & coverage"

release:
	@(git diff --quiet && git diff --cached --quiet) || (echo "You have uncommitted changes - stash or commit your changes"; exit 1)
	@git clean -dxf
	@python setup.py register sdist bdist_wheel upload

test:
	@coverage run test_project/manage.py test pagination --keepdb --verbosity=${VERBOSITY}
	@flake8 .
	@DJANGO_SETTINGS_MODULE=test_project.settings coverage report
