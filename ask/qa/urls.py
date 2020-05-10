# from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'qa'

urlpatterns = [
    url(r'^$', views.get_page, name='home'),
    url(r'^login/$', views.test, name='login'),
    url(r'^signup/$', views.test, name='signup'),
    url(r'^question/(?P<question_id>\d+)/$', views.get_question, name='question'),
    url(r'^ask/$', views.get_ask, name='ask'),
    url(r'^popular/$', views.get_popular, name='popular'),
    url(r'^new/$', views.test, name='new'),
]

'''
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
'''
