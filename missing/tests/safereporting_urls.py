from django.conf.urls import url

# To enable filtering
from missing import debug

def raise_exception(request):
    raise Exception

urlpatterns = [
    url(r'^failure/$', raise_exception, name='failure'),
]
