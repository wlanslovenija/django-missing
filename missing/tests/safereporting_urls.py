from django.conf.urls import patterns, include, url

def raise_exception(request):
    raise Exception

urlpatterns = patterns('',
    url(r'^failure/$', raise_exception, name='failure'),
)
