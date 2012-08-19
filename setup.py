import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name = "Negar",
    version = "0.2",
    author = "Shahin Azad",
    author_email = "ishahinism@gmail.com",
    packages = find_packages() + ['lib'],
    packages_dir = {'Virastar':'lib/Virastar'},
#    py_modules = ['lib.Virastar'],
    scripts=['bin/Negar.py'],
    description = "Negar is a spell corrector and Persian text editor",
    license = "GPL",
    keywords = "spellcheck Persian editor",
    url = "http://shahinism.github.com/Negar",
    #packages = find_packages('', 'lib'),
    long_description=read
    ('README.md'),    
)
