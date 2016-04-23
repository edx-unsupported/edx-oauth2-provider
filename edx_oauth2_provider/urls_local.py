"""
Serve admin and OAuth2 provider urls
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = patterns(
    '',
    url('^oauth2/', include('edx_oauth2_provider.urls', namespace='oauth2')),
    url('^admin/', admin.site.urls),
)
