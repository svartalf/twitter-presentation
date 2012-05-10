# -*- coding: utf-8 -*-

import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')

TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')

DATABASE_PATH = 'postgresql://user:password@localhost/twitter'

try:
    from settings_local import *
except ImportError:
    pass