# Virastar is a python module to check and edit Persian text as good
# as possible. It'll edit punctuation and standard spacing on your
# Persian text.

# To install python-negar module you can read instructor in the Readme
# file. or just can run python setup.py install ;-)

# Copyright (C) <2013> <Shahin Azad [ishahinism at Gmail]>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name="python-negar",
    version="0.6.1",
    author="Shahin Azad",
    author_email="ishahinism@gmail.com",
    maintainer="Alireza Savand",
    maintainer_email="alireza.savand@gmail.com",
    include_package_data=True,
    packages=find_packages() + ['negar'],
    package_dir={'negar': 'negar'},
    package_data={'negar/data': ['data/*.dat']},
    description="Negar is a spell corrector and Persian text editor",
    license="GPL",
    keywords="spellcheck Persian editor",
    url="http://shahinism.github.com/python-negar",
    entry_points={
        'console_scripts': [
            'negar = negar.negar:main',
        ],
    },
    long_description=open("README.md").read(),
)
