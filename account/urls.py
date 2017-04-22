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

	url(r'^profile/', include([
		url(r'^add/$', profile_views.add_profile, name = 'add_profile'),
		url(r'^$', profile_views.profile, name = 'profile_empty'),
		url(r'^(?P<username>\w+)/$', profile_views.profile, name = 'profile'),
		url(r'^(?P<username>\w+)/edit/$', profile_views.EditProfile.as_view(), name = 'edit_profile'),
		url(r'^(?P<username>\w+)/edit/add_skill/$', profile_views.add_skill, name = 'add_skill'),
    ])),

] 