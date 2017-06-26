from django.conf.urls import url

urlpatterns = [
    url(r'^homepage/$', lambda request: None, name='homepage'),
]
