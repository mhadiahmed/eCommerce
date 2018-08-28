from django.conf.urls import url
from .views import (
    PostListView,
    PostDetialView,
    PostUpdateView,
    PostDeleteView,
    PostCreateView
)

urlpatterns = [
    url(r'^$',PostListView.as_view(),name='list' ),
	url(r'^create/$',PostCreateView.as_view() , name='api-create'),
	url(r'^(?P<pk>\d+)$',PostDetialView.as_view() , name='detail'),
	url(r'^(?P<pk>\d+)/edit/$',PostUpdateView.as_view() , name='update'),
	url(r'^(?P<pk>\d+)/delete/$',PostDeleteView.as_view() , name='delete'),
	]
