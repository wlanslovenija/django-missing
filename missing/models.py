from django.conf import settings

try:
    from django import urls
except ImportError:
    from django.core import urlresolvers as urls

# To load docutils extensions somewhere
from missing import admindocs

# NoReverseMatch exceptions are silent (replaced by TEMPLATE_STRING_IF_INVALID setting), but we
# disable this behavior here
if getattr(settings, 'URL_RESOLVERS_DEBUG', False) and getattr(settings, 'DEBUG', False):
    urls.NoReverseMatch.silent_variable_failure = False
