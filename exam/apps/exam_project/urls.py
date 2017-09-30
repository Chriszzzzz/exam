from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$',views.index),
	url(r'^login$',views.login),
	url(r'^logout$', views.logout),
	url(r'^create$', views.create),
	url(r'^register$',views.register),
	url(r'^dashboard$', views.dashboard),
	url(r'^wish_items/create$', views.createpage),
	url(r'^delete/(?P<itemid>\d+)$', views.delete),
	url(r'^wish_items/(?P<itemid>\d+)$', views.info),
	url(r'^addtomylist/(?P<itemid>\d+)$', views.addto),
	url(r'^remove/(?P<authorid>\d+)/(?P<itemid>\d+)$', views.remove),

]