import os

from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(
    name = 'django-missing',
    version = VERSION,
    description = 'Some missing features in Django. Are not missing anymore.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
    author = 'Mitar',
    author_email = 'mitar.django@tnode.com',
    url = 'https://bitbucket.org/mitar/django-missing',
    license = "AGPLv3",
    packages = find_packages(),
    package_data = {
        'missing' : [
            'static/missing/*',
        ],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'django-staticfiles',
    ],
)
