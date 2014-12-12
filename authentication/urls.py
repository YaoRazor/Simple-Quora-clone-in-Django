from django.conf.urls import url, patterns
import authentication.views


urlpatterns = patterns('',
    url(r'^confirm/(?P<activation_key>\w+)/', authentication.views.confirm),
    url(r'^register/$', authentication.views.register, name='register'),
    url(r'^login/$', authentication.views.login, name="login"),
    url(r'^logout/$', authentication.views.logout, name="logout")
)
