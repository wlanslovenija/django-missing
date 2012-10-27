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
