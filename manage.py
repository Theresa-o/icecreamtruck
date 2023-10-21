#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from icecreamtruck.settings import base


def main():
    """Run administrative tasks."""
    # Set DEBUG to True only in the local environment and False in production
    if base.DEBUG:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icecreamtruck.settings.local_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icecreamtruck.settings.production_settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
