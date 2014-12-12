from django.conf.urls import url, patterns
import authentication.views
from django.contrib.auth.views import login


urlpatterns = patterns('',
    #url(r'^confirm/(?P<activation_key>\w+)/', authentication.views.confirm),
    url(r'^register/$', authentication.views.register, name='register'),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', authentication.views.logout, name="logout"),
    url(r'^profile/$', authentication.views.profile, name="profile"),
)
