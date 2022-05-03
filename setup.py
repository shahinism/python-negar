import re

from setuptools import setup, find_packages

version = re.search(
    r'(__version__ = "(\d\.\d(\.\d+)?)")',
    open("negar/constants.py", encoding="utf8").read(),
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
        'regex'
    ],
    package_dir={'negar': 'negar'},
    package_data={'negar/data': ['data/*.dat']},
    description="Negar is a spell corrector and Persian text editor",
    license="GPL",
    keywords="spellcheck Persian editor",
    url="http://github.com/shahinism/python-negar",
    entry_points={
        'console_scripts': [
            'negar = negar.gui:main',
        ],
    },
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],

)
