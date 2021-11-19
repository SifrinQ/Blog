from django.conf.urls import url, include
from .views import add_article, thanks, RegisterView, index, login, logout, articles, update_profile, profile, searching, test_pag

urlpatterns = [
	url(r'^index/$', index, name = 'index'),
	url(r'^index/(?P<id>[0-9]+)/$', articles, name = 'articles'),
	url(r'^index/(?P<id>[0-9]+)/profile/$', profile, name = 'profile'),
	url(r'^index/(?P<id>[0-9]+)/update_profile/$', update_profile, name = 'update_profile'),
	url(r'^index/searching/$', searching, name = 'searching'),
	url(r'^index/test_pag/(?P<page>[0-9]+)$', test_pag, name = 'test_pag'),
	url(r'^register/$', RegisterView.as_view(), name = 'register'),
	url(r'^login/$', login, name = 'login'),
	url(r'^logout/$', logout, name = 'logout'),
	url(r'^add_blog/$', add_article, name='add_article'),
	url(r'^thanks/$', thanks, name='thanks'),
]
