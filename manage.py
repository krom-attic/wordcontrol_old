#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Production settings must be set via environmental variable
    # Running production with dev settings should fail due to lack of dev modules, which are
    # not listed in requirements.txt
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wordcontrol.settings.dev_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
