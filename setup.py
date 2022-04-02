import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

version = re.search(
    r'(__version__ = "(\d\.\d\.\d+)")',
    open("negar/constants.py").read(),
    re.M
).group(2)

setup(
    name="python-negar",
    version=version,
    author="Shahin Azad",
    author_email="ishahinism@gmail.com",
    maintainer="Javad Razavian, Alireza Savand",
    maintainer_email="javadr@gmail.com, alireza.savand@gmail.com",
    include_package_data=True,
    packages=find_packages() + ['negar'],
    install_requires=[
        'pyperclip',
        'PyICU'
    ],
    package_dir={'negar': 'negar'},
    package_data={'negar/data': ['data/*.dat']},
    description="Negar is a spell corrector and Persian text editor",
    license="GPL",
    keywords="spellcheck Persian editor",
    url="http://shahinism.github.com/python-negar",
    entry_points={
        'console_scripts': [
            'negar = negar.gui:main',
        ],
    },
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
)
