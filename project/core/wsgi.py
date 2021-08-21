"""
WSGI config for activity_schedule project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD:project/core/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
>>>>>>> f60d04fd59317778890cf832bfab81159afccb65:project/base/wsgi.py

application = get_wsgi_application()
