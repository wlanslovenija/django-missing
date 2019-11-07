from django.conf import settings
try:
    from django import urls
except ImportError:
    from django.core import urlresolvers as urls
from django.utils import translation

class ForceAdminLanguage(object):
    """
    Middleware which forces language in Django admin to ``ADMIN_LANGUAGE_CODE`` setting value.

    Useful when not wanting that Django content language interferes with admin language,
    especially when admin interface is not translated fully in all languages content is,
    or when error messages in admin interface are hard to debug because of a rare language
    they are displayed in.

    Should be added to ``MIDDLEWARE_CLASSES`` after ``LocaleMiddleware`` middleware::

        MIDDLEWARE_CLASSES = (
            ...
            django.middleware.locale.LocaleMiddleware,
            missing.middleware.ForceAdminLanguage,
            ...
        )
    """

    def process_request(self, request):
        admin_url = urls.reverse('admin:index')
        admin_preview_url = admin_url + 'r/'
        if request.path.startswith(admin_url) and not request.path.startswith(admin_preview_url):
            translation.activate(settings.ADMIN_LANGUAGE_CODE)

        return None
