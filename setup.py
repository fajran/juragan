from setuptools import setup, find_packages

setup(
    name = "juragan",
    version = "0.2",
    url = 'http://www.ubuntu-id.org/',
    license = 'BSD',
    description = 'Distribusi DVD Repository Ubuntu',
    author = 'Fajran Iman Rusadi',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'simplejson', 'markdown']
)

