from django.conf.urls import url
from . import views
app_name = 'core'

urlpatterns = [
    url(r'^register/$',views.register, name='register'),
    url(r'^auth/$',views.auth_view , name='auth'),
    url(r'^ver/$',views.ver , name='ver'),
    url(r'^mudar_senha/(?P<pk>[-\w]+)$',views.change_password , name='mudar_senha'),
    url(r'^prioridades/$',views.prioridades , name='prioridades'),
    url(r'^remover/(?P<pk>[-\w]+)$',views.remover, name='remover'),
    url(r'^terminar/(?P<pk>[-\w]+)$',views.terminar , name='terminar'),
    url(r'^auth_change/$',views.auth_change , name='auth_change'),
    url(r'^editar/(?P<pk>[-\w]+)$',views.Editar.as_view()),
    url(r'^verificar_usuario/$', views.PreChangePassword.as_view()),
    url(r'^home/$', views.Home.as_view()),
    url(r'', views.WelcomeView.as_view()),
	url(r'^login/$', views.WelcomeView.as_view()),
	url(r'^logout/$', views.WelcomeView.as_view()),
]