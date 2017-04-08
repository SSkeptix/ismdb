from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views
from .forms import LoginForm

urlpatterns = [
    url(r'^login/', login, {'template_name': 'account/login.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', logout, {'next_page': '/account/login'}),
    url(r'^register/$', views.register),
    url(r'^$', views.account),
    #url(r'^reset_password/$', views.reset_password, name='reset_password'),

    url(r'^add_skill/$', views.add_skill),
] 