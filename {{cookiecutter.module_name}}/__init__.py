# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) {{ cookiecutter.year }} by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool


def register():
    Pool.register(
        module='{{ cookiecutter.module_name }}', type_='model'
    )
