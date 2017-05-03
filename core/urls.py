from django.conf.urls import url, include
#from .search.views import Search
#from .control.skill.views import AddSkill, EditSkill
from . import views

app_name = 'core'

urlpatterns = [

	url(r'^search/', include([
		url(r'^$', views.test, name = 'search'), #Search.as_view()
		url(r'^(?:page-(?P<page>[\d]+)/)?$', views.test, name = 'search_page'), #Search.as_view()
    ])),

	url(r'^control/', include([
		url(r'^skill/add/$', views.test, name = 'add_skill'), #AddSkill.as_view()
		url(r'^skill/(?P<skill_type>[\w]+)/(?P<id>[\d]+)/edit/$', views.test, name = 'edit_skill'), #EditSkill.as_view()
 
	])),

	

    url(r'^test/$', views.test),

] 
