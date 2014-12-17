from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import CreateView
from photologue.models import Photo

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('authentication.urls', namespace='authentication')),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

