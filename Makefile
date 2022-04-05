#!/bin/fish

VER=$(shell grep __version__ negar/constants.py|cut -d= -f2|tr -d '\" ')

.ONESHELL:

ver:
	@echo python-negar ver. $(VER)

setup: ver
	python setup.py sdist

lins: ver
	python setup.py install

pins: ver
	pip install python-negar==$(VER)

upypi: setup
	twine upload dist/*

utest: setup
	twine upload --repository-url https://test.pypi.org/legacy/  dist/*

compile: ver
	nuitka3 --standalone --onefile --linux-onefile-icon=negar/logo.png \
	--include-data-file=negar/data/untouchable.dat=data/untouchable.dat -o dist/gui-v$(VER).bin \
	--output-dir=dist --remove-output --enable-plugin=pyqt6 negar/gui.py
	ls -l dist

pyins: ver
	rm build/gui/ -rfv
	. .negar/bin/activate
	pyinstaller -p negar --onefile --add-data negar/data/untouchable.dat:data --noupx negar/gui.py
	ls -l /dist

clean: ver
	rm python_negar.egg-info/ -rfv
	rm build/ -rfv
	rm dist/ -rfv
	rm gui.build/ -rfv
	rm gui.dist/ -rfv
