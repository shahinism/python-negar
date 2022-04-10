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
	twine upload dist/python-negar-$(VER).tar.gz

utest: setup
	twine upload --repository-url https://test.pypi.org/legacy/  dist/python-negar-$(VER).tar.gz

upload: setup upypi utest

nuCompile: ver
	nuitka3 --standalone --onefile --linux-onefile-icon=negar/logo.png \
	--include-data-file=negar/data/untouchable.dat=data/untouchable.dat \
	--include-data-dir=.negar/lib/python3.10/site-packages/pyuca=pyuca \
	-o dist/negar-gui-v$(VER).bin \
	--output-dir=dist --remove-output --enable-plugin=pyqt5 negar/gui.py
	ls -lh dist

piCompile: ver
	rm build/gui/ -rfv
	. .negar/bin/activate
	pyinstaller -p negar --onefile --add-data negar/data/untouchable.dat:data \
	--collect-data pyuca --noupx negar/gui.py -n negar-gui-v$(VER)
	ls -lh dist

clean: ver
	rm python_negar.egg-info/ -rfv
	rm build/ -rfv
	rm dist/ -rfv
	rm gui.build/ -rfv
	rm gui.dist/ -rfv
