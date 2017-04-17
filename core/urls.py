from django.conf.urls import url, include
from . import views

app_name = 'core'

urlpatterns = [

	url(r'^search/', include([
		url(r'^$', views.search, name = 'search'),
		url(r'^(?:page-(?P<page>[\d]+)/)?$', views.search, name = 'search_page'),
    ])),

    url(r'^test/$', views.test),

] 
