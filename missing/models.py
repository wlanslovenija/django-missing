from django.conf import settings

try:
    # Importing from django.core.urlresolvers is deprecated in favor of django.urls
    from django.urls import urlresolvers
except ImportError:
    from django.core import urlresolvers

# To load docutils extensions somewhere
from missing import admindocs

# NoReverseMatch exceptions are silent (replaced by TEMPLATE_STRING_IF_INVALID setting), but we
# disable this behavior here
if getattr(settings, 'URL_RESOLVERS_DEBUG', False) and getattr(settings, 'DEBUG', False):
    urlresolvers.NoReverseMatch.silent_variable_failure = False
