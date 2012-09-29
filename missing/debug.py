import re

from django.views import debug

debug.HIDDEN_SETTINGS = re.compile(debug.HIDDEN_SETTINGS.pattern + '|URL|CSRF|COOKIE')

class SafeExceptionReporterFilter(debug.SafeExceptionReporterFilter):
    """
    Safe exception reporter filter which also filters password from
    request environment (META).
    """

    def get_post_parameters(self, request):
        # We hook into this method to modify request in place, not nice, but it works
        for key in request.META:
            if key.isupper():
                request.META[key] = debug.cleanse_setting(key, request.META[key])

        return super(SafeExceptionReporterFilter, self).get_post_parameters(request)
