try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name="python-negar",
    version="0.6.7",
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
            'negar = negar.gui:main',
        ],
    },
    long_description=open("README.md").read(),
)
