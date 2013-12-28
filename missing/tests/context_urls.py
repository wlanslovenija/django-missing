from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^homepage/$', lambda request: None, name='homepage'),
)
