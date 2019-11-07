#!/usr/bin/env python

import os

from setuptools import setup, find_packages

try:
    # Workaround for http://bugs.python.org/issue15881
    import multiprocessing
except ImportError:
    pass

VERSION = '1.0.0'

if __name__ == '__main__':
    setup(
        name = 'django-missing',
        version = VERSION,
        description = 'Some missing features in Django. Are not missing anymore.',
        long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
        author = 'Mitar',
        author_email = 'development@wlan-si.net',
        url = 'https://github.com/wlanslovenija/django-missing',
        license = "AGPLv3",
        packages = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests')),
        package_data = {},
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
            'Django>=1.11.26',
        ],
        test_suite = 'tests.runtests.runtests',
    )
