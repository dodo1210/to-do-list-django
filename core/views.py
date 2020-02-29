from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from .models import Tasks as Taskss
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.core.mail import send_mail
from datetime import datetime,timezone
from django.contrib.auth.decorators import login_required

def auth_view(request):
  username = request.POST.get('username','')
  password = request.POST.get('password','')
  print(username)
  user  = auth.authenticate(username=username, password=password)
  if user is not None:
    auth.login(request, user)
    return HttpResponseRedirect('/home/')
  else:
    c = {}
    c.update(csrf(request))
    c.update({'error_message': 'Senha ou Usuario Incorretos'})
    return render(request, 'index.html', c)

def auth_change(request):
  email = request.POST.get('email','')
  user = User.objects.get(email=email)
  if email == user.email:
    return HttpResponseRedirect('/mudar_senha/'+str(user.pk))
  else:
    return HttpResponse('auth_change')

def logout(request):
  c = {}
  c.update(csrf(request))
  auth.logout(request)
  return render_to_response('index.html',c)

def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/')
  else:
    form = RegisterForm()
  context = {
    'form' : form
  }
  return render(request,'cadastro.html',context)

@login_required
def change_password(request,pk):
  user = User.objects.get(id=pk)
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)
    if form.is_valid():
      form.save()
      print("oi")
      update_session_auth_hash(request, user)
      return HttpResponseRedirect('/') 
    else:
      print("nao")
      return HttpResponseRedirect('/mudar_senha/'+str(pk))
  else:
    form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'mudar_senha.html', args)

@login_required
def ver(request):
  return render(request, 'ver.html',{'tasks':Taskss.objects.all()})

@login_required
def prioridades(request):
  tasks = Taskss.objects.all()
  date = []
  count = 0
  for t in tasks:
    if t.markup == False:
      date.append(str(t.end))
      count+=1
    elif str(t.begin).split('-')[2].split(' ')[0] == str(datetime.now()).split('-')[2].split(' ')[0]:
      date.append(str(t.end))
  date_sort = []
  for d in sorted(date): 
    date_sort.append(d)
  email(request,date_sort[::-1])
  return HttpResponseRedirect('/ver/') 

@login_required
def email(request,date_sort):
  tasks = Taskss.objects.all()
  tarefa = 'As tarefas mais prioritárias são: '
  count = 0

  for d in date_sort:
    for t in tasks:
      if str(t.end) == str(d):
        tarefa+=' '+t.title+' que finaliza '+str(t.end)+'\n'
        break
      elif d.split('-')[2].split(' ')[0] == str(datetime.now()).split('-')[2].split(' ')[0] and t.markup == True:
        tarefa+=' '+t.title+' foi finalizada hoje '+str(t.end)+'\n'
        break

  subject = request.POST.get('subject', 'FINALIZAÇÃO DE TAREFA')
  message = request.POST.get('message', tarefa)
  from_email = request.POST.get('from_email', 'contatoiatrader@gmail.com')
  if subject and message and from_email:
    try:
      send_mail(subject, message, from_email, ['contatodouglassiqueira@gmail.com'])
    except BadHeaderError:
      return HttpResponse('Não foi possível enviar email')

@login_required
def terminar(request,pk):
  tasks = Taskss.objects.get(id=pk)
  subject = request.POST.get('subject', 'FINALIZAÇÃO DE TAREFA')
  message = request.POST.get('message', 'A tarefa '+tasks.title+' foi finalizada')
  from_email = request.POST.get('from_email', 'contatoiatrader@gmail.com')
  if subject and message and from_email:
    try:
      send_mail(subject, message, from_email, ['contatodouglassiqueira@gmail.com'])
    except BadHeaderError:
      return HttpResponse('Invalid header found.')
    tasks.markup = True
    tasks.save()
    return HttpResponseRedirect('/ver/')
  else:
    return HttpResponse('Make sure all fields are entered and valid.')  
  return HttpResponseRedirect('/ver/')

@login_required
def remover(request,pk):
  tasks = Taskss.objects.get(id=pk)
  tasks.delete()
  return HttpResponseRedirect('/ver/')

class Home(CreateView):
  template_name = 'home.html'
  model = Taskss
  fields = ['user','title','description','markup','begin','end']
  success_url = '/ver/'

class WelcomeView(TemplateView):
  def get(self,request):
    template_name = 'index.html'
    form = RegisterForm(request.POST)
    return render(request, template_name)

class PreChangePassword(TemplateView):
  def get(self,request):
    template_name = 'pre_mudar_senha.html'
    form = RegisterForm(request.POST)
    return render(request, template_name)

class Editar(UpdateView):
  model = Taskss
  template_name = 'editar.html'
  form_class = Tasks
  success_url = '/ver/'

class Remover(DeleteView):
  model = Taskss
  success_url = '/ver/'
  
    

