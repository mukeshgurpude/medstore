"""
WSGI config for medical project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical.settings')

# StaticFileHandler is required or else, it will fail to load css, javascript files when debug set to false
application = StaticFilesHandler(get_wsgi_application())
