#!/bin/bash

VER=$(shell grep __version__ negar/constants.py|cut -d= -f2|tr -d '\" '|head -1)

.ONESHELL:

ver:
	@echo python-negar ver. "$(VER)"

.PHONY: uninstall
uninstall:
	@echo "Uninstalling python-negar ..."
	pip uninstall python-negar

setup: ver
	python setup.py sdist
	python setup.py bdist_wheel

lins: ver setup
	pip install "dist/python_negar-$(VER)-py3-none-any.whl"

pins: ver
	pip install python-negar=="$(VER)"

upypi: setup
	twine upload "dist/python-negar-$(VER).tar.gz"

utest: setup
	twine upload -r testpypi "dist/python-negar-$(VER).tar.gz"

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
