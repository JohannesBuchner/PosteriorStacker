.PHONY: clean clean-test clean-pyc clean-build docs help show
.DEFAULT_GOAL := help
.SECONDARY:

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

PYTHON := python3

BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-doc ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.so' -exec rm -f {} +
	find . -name '*.c' -exec rm -f {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-doc:
	rm -rf data.txt posteriorsamples.txt* README.html posteriors_x1.txt.gz 

lint: ## check style with flake8
	flake8 snowline tests

test: ## run tests quickly with the default Python
	${PYTHON} tutorial/run.py
	rst2html5.py README.rst > README.html

test-all: ## run tests on every Python version with tox
	tox

flatdist.txt.gz: Makefile
	#python3 -c 'import numpy; numpy.savetxt("flatdist.txt.gz", numpy.random.normal(3.14,0.1,size=(30,100)))'
	${PYTHON} -c 'import numpy; numpy.savetxt("flatdist.txt.gz", numpy.vstack((numpy.random.normal(3.14,0.1,size=(30,1000)), numpy.random.uniform(2, 4, size=(1000,1000)))))'

flatdist.txt.gz_out_gauss/plots/corner.pdf: flatdist.txt.gz
	${PYTHON} posteriorstacker.py flatdist.txt.gz 2.5 4 4

show: flatdist.txt.gz_out_gauss/plots/corner.pdf
	xdg-open $^

coverage: ## check code coverage quickly with the default Python
	coverage run --source snowline -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	python3 tutorial/run.py && rst2html5.py README.rst > README.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload -s dist/*.tar.gz

dist: clean ## builds source and wheel package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	$(PYTHON) setup.py install
