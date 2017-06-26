from django import http
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


def bad_request_view(request, exception=None):
    """
    Displays 400 bad request page.

    It is similar to the Django built-in ``django.views.defaults.permission_denied`` view,
    but always uses a template and a request context.
    You can configure Django to use this view by adding to ``urls.py``::

        handler400 = 'missing.views.bad_request_view'

    Template should not require a CSRF token.
    """

    t = loader.get_template('400.html')

    return http.HttpResponseBadRequest(t.render(request=request, context={
        'DEBUG': settings.DEBUG,
        'exception': str(exception) if exception else None,
    }), content_type='text/html')


def forbidden_view(request, exception=None, reason=''):
    """
    Displays 403 forbidden page. For example, when request fails CSRF protection.

    It is similar to a merged Django built-in ``django.views.defaults.permission_denied`` and
    ``django.views.csrf.csrf_failure`` views, but always uses a template and a request context.
    You can configure Django to use this view by adding to ``urls.py``::

        handler403 = 'missing.views.forbidden_view'

    and to ``settings.py``::

        CSRF_FAILURE_VIEW = 'missing.views.forbidden_view'

    Template should not require a CSRF token.
    """

    from django.middleware import csrf

    t = loader.get_template('403.html')

    return http.HttpResponseForbidden(t.render(request=request, context={
        'DEBUG': settings.DEBUG,
        'reason': reason,
        'no_referer': reason == csrf.REASON_NO_REFERER,
        'no_cookie': reason == csrf.REASON_NO_CSRF_COOKIE,
        'exception': str(exception) if exception else None,
    }), content_type='text/html')
