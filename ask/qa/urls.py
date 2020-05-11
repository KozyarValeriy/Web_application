# from django.urls import path
from django.conf.urls import url
# from django.contrib.auth.views import login

from . import views

app_name = 'qa'

urlpatterns = [
    url(r'^$', views.get_page, name='home'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^logintest/$', login, name='logintest'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^question/(?P<question_id>\d+)/$', views.get_question, name='question'),
    url(r'^ask/$', views.get_ask, name='ask'),
    url(r'^popular/$', views.get_popular, name='popular'),
    url(r'^new/$', views.test, name='new'),
]
