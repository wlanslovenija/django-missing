import django
from django.conf import settings
from django.core import urlresolvers
from django.template import base

# To load docutils extensions somewhere
from missing import admindocs

if django.VERSION < (1, 9):
    # To be able to force use of "contextblock" tag immediately after "extends" tag, we add it to built-in tags
    base.add_to_builtins('missing.templatetags.context_tags')

# NoReverseMatch exceptions are silent (replaced by TEMPLATE_STRING_IF_INVALID setting), but we
# disable this behavior here
if getattr(settings, 'TEMPLATE_URL_RESOLVERS_DEBUG', False) and getattr(settings, 'TEMPLATE_DEBUG', False):
    urlresolvers.NoReverseMatch.silent_variable_failure = False
