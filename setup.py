import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name = "Negar",
    version = "0.2",
    author = "Shahin Azad",
    author_email = "ishahinism@gmail.com",
    include_package_data=True,
    packages = find_packages() + ['negar'],
    package_dir={'negar': 'negar'},
    package_data={'negar/data': ['data/*.dat']},
    description = "Negar is a spell corrector and Persian text editor",
    license = "GPL",
    keywords = "spellcheck Persian editor",
    url = "http://shahinism.github.com/Negar",
    #packages = find_packages('', 'lib'),
    entry_points={
        'console_scripts': [
            'negar = negar.Negar:main',
        ],
    },
    long_description=read
    ('README.txt'),    
)
