"""WSGI config for the swamp project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swamp.settings")

application = get_wsgi_application()
