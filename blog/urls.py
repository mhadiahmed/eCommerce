from django.conf.urls import url
from django.contrib.auth.views import (
	password_reset,password_reset_done,
	password_reset_confirm,password_reset_complete)
from . import views

urlpatterns = [
	url(r'^$', views.index , name='home'),
	url(r'^contact/$',views.contact , name='contact'),
	url(r'^direct/$',views.direct , name='direct'),
	url(r'^about/$',views.about , name='about'),
	url(r'^create/$',views.create , name='create'),
	url(r'^car/$',views.car , name='car'),
	url(r'^phone/$',views.Phone , name='Phone'),
	url(r'^laptop/$',views.Laptop , name='Laptop'),
	url(r'^jops/$',views.Jops , name='Jops'),
	url(r'^electronic/$',views.Electronic , name='Electronic'),
	url(r'^clothes/$',views.Clothes , name='Clothes'),
	url(r'^makeup/$',views.Makeup , name='Makeup'),
	url(r'^furnishings/$',views.Furnishings , name='Furnishings'),
	url(r'^books/$',views.books , name='books'),
	url(r'^sports/$',views.sports , name='sports'),
	url(r'^property/$',views.Property , name='Property'),
	url(r'^other/$',views.Other , name='Other'),
	url(r'^Pay/$',views.buy , name='Pay'),
	url(r'^profile/$',views.profile , name='profile'),
	url(r'^profile/(?P<pk>\d+)/$',views.profile , name='profile_pk'),
	url(r'^edit/profile/$',views.editProfile , name='edit_profile'),
	url(r'^edit/password/$',views.ChangePassword , name='change_password'),
	url(r'^password-reset/done/$',password_reset_done ,{'template_name':'blog/password/password_sent.html'}, name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm ,{'template_name':'blog/password/password_confirm.html'}, name='password_reset_confirm'),
	url(r'^password-reset/$',password_reset,{'template_name':'blog/password/password_reset.html'} , name='password-reset'),
	url(r'^password_reset/complete/$',password_reset_complete,{'template_name':'blog/password/password_complete.html'} , name='password_reset_complete'),
	url(r'^(?P<id>\d+)$',views.detail , name='detail'),
	url(r'^(?P<id>\d+)/edit/$',views.update , name='update'),
	url(r'^(?P<id>\d+)/delete/$',views.delete , name='delete'),

]
