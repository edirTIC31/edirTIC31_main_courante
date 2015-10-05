#!/usr/bin/env python

import os
from os.path import dirname, abspath, join, isfile
import sys


if __name__ == "__main__":

    BASE_DIR = dirname(abspath(__file__))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edirtic.local_settings" if isfile(join(BASE_DIR, 'edirtic/local_settings.py')) else "edirtic.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
