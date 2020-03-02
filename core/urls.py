from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [ 
    url(r'^mudar_senha/(?P<pk>[-\w]+)$',views.change_password , name='mudar_senha'),
    url(r'^prioridades/(?P<pk>[-\w]+)$',views.prioridades , name='prioridades'),
    url(r'^remover/(?P<pk>[-\w]+)$',views.remover, name='remover'),
    url(r'^sub_tarefa/(?P<pk>[-\w]+)$',views.sub_task,name='sub_tarefa'),
    url(r'^ver_tarefa/(?P<pk>[-\w]+)$',views.view_sub_task,name='ver_tarefa'),
    url(r'^terminar/(?P<pk>[-\w]+)$',views.terminar , name='terminar'),
    url(r'^datas/(?P<pk>[-\w]+)/(?P<date>[\w\-]+)$',views.date_interview , name='datas'),
    url(r'^remover_tarefa/(?P<pk>[-\w]+)$',views.remover_tarefa , name='remover_tarefa'),

    url(r'^register/$',views.register, name='register'),
    url(r'^auth/$',views.auth_view , name='auth'),
    url(r'^ver/$',views.ver , name='ver'),
    url(r'^auth_change/$',views.auth_change , name='auth_change'),
    
    url(r'^editar_tarefa/(?P<pk>[-\w]+)$',views.EditarTarefa.as_view()),
    url(r'^editar/(?P<pk>[-\w]+)$',views.Editar.as_view()),
    url(r'^verificar_usuario/$', views.PreChangePassword.as_view()),
    url(r'^home/$', views.Home.as_view()),
    url(r'^tarefas/(?P<pk>[-\w]+)$', views.Tarefas.as_view()),
    url(r'', views.WelcomeView.as_view()),
    url(r'^login/$', views.WelcomeView.as_view()),
    url(r'^logout/$', views.WelcomeView.as_view()),
]