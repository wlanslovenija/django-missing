from django.conf.urls import url

urlpatterns = [
    url(r'^test1/$', lambda request: None, name='test1'),
    url(r'^test_args/(\d{4})/(\d{2})/(\d+)/$', lambda request: None, name='test_args'),
    url(r'^test_kwargs/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', lambda request: None, name='test_kwargs'),
    url(r'^test_mixed/(?P<year>\d{4})/(\d{2})/(?P<day>\d+)/$', lambda request: None, name='test_mixed'),
    url(r'^test_possible/(?P<year>\d{4})/(?P<day>\d+)/$', lambda request: None, name='test_possible'),
    url(r'^test_possible/(?P<month>\d{2})/(?P<day>\d+)/$', lambda request: None, name='test_possible'),
    url(r'^api/(?P<api_name>v1)/(?P<resource_name>user)/schema/$', lambda request: None, name='api_get_schema'),
    url(r'^some/view/(?P<arg1>.*)/(?P<arg2>.*)/(?P<param>.*)/$', lambda request: None, name='view_name'),
]
