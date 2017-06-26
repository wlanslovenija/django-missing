from django.conf import settings
from django.core import urlresolvers

# To load docutils extensions somewhere
from missing import admindocs

# NoReverseMatch exceptions are silent (replaced by TEMPLATE_STRING_IF_INVALID setting), but we
# disable this behavior here
if getattr(settings, 'URL_RESOLVERS_DEBUG', False) and getattr(settings, 'DEBUG', False):
    urlresolvers.NoReverseMatch.silent_variable_failure = False
