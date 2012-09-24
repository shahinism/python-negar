import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

dependecy = [] # list of dependencies That negar needs to install

# Here we check if PySide is not installed then install it with pypi ;-)
try:
    import PyQt4
except ImportError:
    #dependecy.append("PyQt4")
    print "Negar needs PyQt4 to run gui\nplease install it and try again."
    exit(1)
    
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name = "Negar",
    version = "0.6",
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
    install_requires = dependecy,
    entry_points={
        'console_scripts': [
            'negar = negar.Negar:main',
        ],
    },
    long_description=read
    ('README.txt'),    
)
