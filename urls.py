from django.conf.urls.defaults import *

# For testing / example only
urlpatterns = patterns('jsforms.views',
    url(r'^test/$', 'test', name='test'),
)
