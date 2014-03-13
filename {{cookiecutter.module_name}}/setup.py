#!/usr/bin/env python
import re
import os
import sys
import time
import unittest
import ConfigParser
from setuptools import setup, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PostgresTest(Command):
    """
    Run the tests on Postgres.
    """
    description = "Run tests on Postgresql"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from trytond.config import CONFIG
        CONFIG['db_type'] = 'postgresql'
        CONFIG['db_host'] = 'localhost'
        CONFIG['db_port'] = 5432
        CONFIG['db_user'] = 'postgres'

        from trytond import backend
        import trytond.tests.test_tryton

        # Set the db_type again because test_tryton writes this to sqlite
        # again
        CONFIG['db_type'] = 'postgresql'

        trytond.tests.test_tryton.DB_NAME = 'test_' + str(int(time.time()))
        from trytond.tests.test_tryton import DB_NAME
        trytond.tests.test_tryton.DB = backend.get('Database')(DB_NAME)
        from trytond.pool import Pool
        Pool.test = True
        trytond.tests.test_tryton.POOL = Pool(DB_NAME)

        from tests import suite
        test_result = unittest.TextTestRunner(verbosity=3).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-1)


config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []

MODULE2PREFIX = {}


for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append(
            '%s_%s >= %s.%s, < %s.%s' % (
                MODULE2PREFIX.get(dep, 'trytond'), dep,
                major_version, minor_version, major_version,
                minor_version + 1
            )
        )
requires.append(
    'trytond >= %s.%s, < %s.%s' % (
        major_version, minor_version, major_version, minor_version + 1
    )
)
setup(
    name="{{ cookiecutter.module_name }}",
    version=info.get('version', '0.0.1'),
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter.author }}",
    author_email="{{ cookiecutter.email }}",
    url="{{ cookiecutter.website }}",
    package_dir={'trytond.modules.{{ cookiecutter.module_name }}': '.'},
    packages=[
        'trytond.modules.{{ cookiecutter.module_name }}',
        'trytond.modules.{{ cookiecutter.module_name }}.tests',
    ],
    package_data={
        'trytond.modules.{{ cookiecutter.module_name }}': info.get('xml', [])
        + info.get('translation', [])
        + ['tryton.cfg', 'locale/*.po', 'tests/*.rst', 'reports/*.odt']
        + ['view/*.xml'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Tryton',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    {{ cookiecutter.module_name }} = trytond.modules.{{ cookiecutter.module_name }}
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    cmdclass={
        'test_on_postgres': PostgresTest,
    }
)
