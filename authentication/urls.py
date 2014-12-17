from django.conf.urls import url, patterns
import authentication.views
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    #url(r'^confirm/(?P<activation_key>\w+)/', authentication.views.confirm),
    url(r'^register/$', authentication.views.register_user, name='register_user'),
    url(r'^register_success/$', authentication.views.register_success, name='register_success'),
    url(r'^login/$', login, name="login"),
    # url(r'^logout/$', authentication.views.logout, name="logout"),
    url(r'^logout/$', authentication.views.logout, name="logout"),
    url(r'^logout_success/$', authentication.views.logout_success, name="logout_success"),
    url(r'^profile/$', authentication.views.profile, name="profile"),
)
