from django.conf.urls import url, include
from .search.views import Search
from .control.add_skill.views import AddSkill
from . import views

app_name = 'core'

urlpatterns = [

	url(r'^search/', include([
		url(r'^$', Search.as_view(), name = 'search'),
		url(r'^(?:page-(?P<page>[\d]+)/)?$', Search.as_view(), name = 'search_page'),
    ])),

	url(r'^control/', include([
		url(r'^add_skill/$', AddSkill.as_view(), name = 'add_skill'),

	])),

	

    url(r'^test/$', views.test),

] 
