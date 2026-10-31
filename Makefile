#!/bin/bash

VER=$(shell grep __version__ negar/constants.py|cut -d= -f2|tr -d '\" '|head -1)

.ONESHELL:

# use uv when it is available, fall back to pip/setup.py otherwise
UV := $(shell command -v uv 2>/dev/null)
ifdef UV
PIP := uv pip
REFRESH := --refresh  # a just-uploaded version is otherwise hidden by uv's cached index
else
PIP := pip
endif

ver:
	@echo python-negar ver. "$(VER)"

.PHONY: uninstall
uninstall:
	@echo "Uninstalling python-negar ..."
	$(PIP) uninstall python-negar

setup: ver
ifdef UV
	uv build
else
	python setup.py sdist
	python setup.py bdist_wheel
endif

lins: ver setup
	$(PIP) install "dist/python_negar-$(VER)-py3-none-any.whl"

pins: ver
	$(PIP) install $(REFRESH) python-negar=="$(VER)"

upypi: setup
	twine upload "dist/python_negar-$(VER).tar.gz"

utest: setup
	twine upload -r testpypi "dist/python_negar-$(VER).tar.gz"

upload: setup upypi utest

test:
	python -m unittest discover tests

clean:
	@rm python_negar.egg-info/ -rfv
	@rm build/ -rfv
	@rm dist/ -rfv
	@rm gui.build/ -rfv
	@rm gui.dist/ -rfv
	@rm negar*.spec -rfv
