from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^(?P<id>\d+)/$',views.thread , name='thread'),
	url(r'^(?P<id>\d+)/delete/$',views.comment_delete ,name='deletee'),

]