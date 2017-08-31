#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-thesaurus',
    version='0.0.1',
    packages=['thesaurus'],
    include_package_data=True,
    license='MIT License',
    description='A Django app for importing and using thesauri.',
    long_description=README,
    url='https://github.com/City-of-Helsinki/django-thesaurus',
    author='Mikko Keskinen',
    author_email='keso@iki.fi',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-django',
    ],
    install_requires=[
        'Django',
        'django-parler',
        'rdflib',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
