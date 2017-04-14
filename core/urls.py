from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
	url(r'^search/$', views.search, name = 'search'),
	url(r'^search/(?P<username>\w+)/$', views.search),


] 