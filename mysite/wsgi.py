"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# PORTING: These two lines are useful when serving static files and templates on Heroku
# if develop locally, skip these two lines
from dj_static import Cling
application = Cling(get_wsgi_application())
