from django.conf.urls import url, include
from .search.views import Search
from .control.skill.views import AddSkill, EditSkill
from . import views

app_name = 'core'

urlpatterns = [

	url(r'^search/', include([
		url(r'^$', Search.as_view(), name = 'search'),
		url(r'^(?:page-(?P<page>[\d]+)/)?$', Search.as_view(), name = 'search_page'),
    ])),

	url(r'^control/', include([
		url(r'^skill/add/$', AddSkill.as_view(), name = 'add_skill'),
		url(r'^skill/(?P<skill_type>[\w]+)/(?P<id>[\d]+)/edit/$', EditSkill.as_view(), name = 'edit_skill'),

	])),

	

    url(r'^test/$', views.test),

] 
