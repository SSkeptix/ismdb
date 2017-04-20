from django.conf.urls import url, include
from . import views
from .control.add_skill.views import AddSkill

app_name = 'core'

urlpatterns = [

	url(r'^search/', include([
		url(r'^$', views.search, name = 'search'),
		url(r'^(?:page-(?P<page>[\d]+)/)?$', views.search, name = 'search_page'),
    ])),

	url(r'^control/', include([
		url(r'^add_skill/$', AddSkill.as_view(), name = 'add_skill'),

	])),

	

    url(r'^test/$', views.test),

] 
