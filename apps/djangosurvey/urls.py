from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
    url(r'^$', views.home),
	url(r'^check_login$', views.check_login),
	url(r'^check_register$', views.check_register),
    url(r'^dashboard$', views.dashboard),
    url(r'^add/item$', views.add_item),
	url(r'^check_item$', views.check_item),
    url(r'^wish/items/(?P<id>\d+)$', views.show_item),
	url(r'^wish/add/(?P<id>\d+)$', views.add_wishlist),
	url(r'^remove/wish/(?P<id>\d+)$', views.remove_wish),
	url(r'^delete/item/(?P<id>\d+)$', views.delete_item),
    url(r'^logout$', views.logout),
]
