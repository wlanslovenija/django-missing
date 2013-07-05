from django import http, template
from django.conf import settings
from django.template import loader
from django.utils import decorators
from django.views.decorators import csrf

class EnsureCsrfCookieMixin(object):
    """
    Mixin for Django class-based views which forces a view to send the CSRF cookie.

    This is useful when using Ajax-based sites which do not have an HTML form with
    a :tag:`csrf_token` that would cause the required CSRF cookie to be sent.
    """

    @decorators.method_decorator(csrf.ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)

def forbidden_view(request, reason=''):
    """
    Displays 403 forbidden page. For example, when request fails CSRF protection.

    Similar to Django built-in view, but using template and request context. You can
    configure Django to use by adding to ``urls.py``::

        handler403 = 'missing.views.forbidden_view'

    and to ``settings.py``::

        CSRF_FAILURE_VIEW = 'missing.views.forbidden_view'
    """

    from django.middleware import csrf
    t = loader.get_template('403.html')
    return http.HttpResponseForbidden(t.render(template.RequestContext(request, {
        'DEBUG': settings.DEBUG,
        'reason': reason,
        'no_referer': reason == csrf.REASON_NO_REFERER,
    })))
