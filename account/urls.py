from django.conf.urls import url, include
from . import views
from .profile import views as profile_views
from .forms import Login as LoginForm
from django.contrib.auth.views import login, logout


app_name = 'account'

urlpatterns = [
	url(r'^login/', login, {'template_name': 'account/login.html', 'authentication_form': LoginForm}, name = 'login'),
	url(r'^logout/$', logout, {'next_page': 'account:login'}, name = 'logout'),
	url(r'^register/$', views.register, name = 'register'),

	url(r'^profile/$', profile_views.profile, name = 'profile'),
	url(r'^profile/add/$', profile_views.add_profile, name = 'add_profile'),
	url(r'^profile/(?P<username>\w+)/$', profile_views.profile),
	url(r'^profile//edit/$', profile_views.edit_profile, name = 'edit_profile'),
	url(r'^profile/(?P<username>\w+)/edit/$', profile_views.edit_profile),
	url(r'^profile//edit/add_skill/$', profile_views.add_skill, name = 'add_skill'),
	url(r'^profile/(?P<username>\w+)/edit/add_skill/$', profile_views.add_skill),

] 