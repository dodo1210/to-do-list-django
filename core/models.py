from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User
from datetime import datetime

# Create your models here.

class MainTasks(models.Model):
	title = models.CharField(max_length=60, blank=True)

class Tasks(models.Model):
	user = models.ManyToManyField(User, related_name='Criador')
	title = models.CharField(max_length=60, blank=True)
	description = models.TextField(verbose_name='Descrição', blank=True)
	markup = models.BooleanField(verbose_name='Terminado',default=False)
	begin = models.DateTimeField(verbose_name='Data de Início',default=timezone.now)
	end = models.DateTimeField(verbose_name='Data de Fim',default=timezone.now)
	markup_end = models.DateTimeField(verbose_name='Data de Termino',default=timezone.now,blank=True)
	main_task = models.ForeignKey(MainTasks, default=1, blank=False, on_delete = models.CASCADE,verbose_name='Tarefa Principal')

	

