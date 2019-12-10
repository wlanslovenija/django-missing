import re

from django.views import debug

# We use a negative lookbehind to not escape "wsgi.url_scheme" which is used as source for request schema.
debug.HIDDEN_SETTINGS = re.compile(debug.HIDDEN_SETTINGS.pattern + r'|(?<!wsgi\.)URL|CSRF|COOKIE|csrftoken|csrfmiddlewaretoken|sessionid', re.IGNORECASE)

class SafeExceptionReporterFilter(debug.SafeExceptionReporterFilter):
    """
    Safe exception reporter filter which also filters request environment
    (``META``) and cookies (``COOKIES``) so that it is safer to share the
    report publicly.

    This is useful to not display passwords and other sensitive data passed to
    Django through its process environment.

    Furthermore, it configures Django to additionally clean settings with ``URL``, ``CSRF``,
    ``COOKIE``, ``csrftoken``, ``csrfmiddlewaretoken``, and ``sessionid`` in keys.

    To install it, configure Django to::

        DEFAULT_EXCEPTION_REPORTER_FILTER = 'missing.debug.SafeExceptionReporterFilter'

    and import ``missing.debug`` somewhere in your code, for example, in ``urls.py``
    of your project.
    """

    def get_post_parameters(self, request):
        if request is None:
            return super(SafeExceptionReporterFilter, self).get_post_parameters(request)

        # We hook into this method to modify request in place, not nice, but it works.
        for key in request.META:
            request.META[key] = debug.cleanse_setting(key, request.META[key])
        for key in request.COOKIES:
            request.COOKIES[key] = debug.cleanse_setting(key, request.COOKIES[key])

        post = super(SafeExceptionReporterFilter, self).get_post_parameters(request).copy()

        for key in post:
            post[key] = debug.cleanse_setting(key, post[key])

        return post
