import os
from os.path import dirname, abspath, join, isfile


def define_default_settings():

    BASE_DIR = dirname(abspath(__file__))

    if isfile(join(BASE_DIR, 'local_settings.py')):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edirtic.local_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edirtic.settings")
