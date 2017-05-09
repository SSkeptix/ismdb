from django.conf.urls import url, include
from . import views
from .profile import views as profile_views
from .forms import Login as LoginForm
from django.contrib.auth.views import (
    login, 
    logout, 
    password_reset, 
    password_reset_done, 
    password_reset_confirm,
    password_reset_complete
)

app_name = 'account'



urlpatterns = [
	url(r'^login/', login, {'template_name': 'account/login.html', 'authentication_form': LoginForm}, name = 'login'),
	url(r'^logout/$', logout, {'next_page': 'account:login'}, name = 'logout'),
	url(r'^register/$', views.register, name = 'register'),

	url(r'^profile/', include([
		url(r'^add/$', profile_views.add_profile, name = 'add_profile'),
		url(r'^$', profile_views.Profile.as_view(), name = 'profile_empty'),
		url(r'^(?P<username>[\w@.+-]+)/$', profile_views.Profile.as_view(), name = 'profile'),
    	url(r'^(?P<username>[\w@.+-]+)/edit/$', profile_views.EditProfile.as_view(), name = 'edit_profile'),
    ])),

    url(r'^change-password/$', views.change_password, name='change_password'),
    
    url(r'^reset-password/$', password_reset, {'template_name': 'account/reset_password.html', 'post_reset_redirect': 'account:password_reset_done', 'email_template_name': 'account/reset_password_email.html'}, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'account/reset_password_done.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'account/reset_password_confirm.html', 'post_reset_redirect': 'account:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'account/reset_password_complete.html'}, name='password_reset_complete'),

    ]