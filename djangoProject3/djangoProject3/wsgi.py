"""
Team Members
Manmeet Kaur - C0884039
Angrej Singh - C0884026
Riya Sidhu - C0886435
Dheepasri Ravichandran - C0883900
WSGI config for djangoProject3 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject3.settings')

application = get_wsgi_application()
