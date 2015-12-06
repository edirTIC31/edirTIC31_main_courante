#!/usr/bin/env python

import sys

from edirtic.utils import define_default_settings


if __name__ == "__main__":

    define_default_settings()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
