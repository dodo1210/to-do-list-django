from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Tasks as Taskss
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf

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

def logout(request):
  c = {}
  c.update(csrf(request))
  auth.logout(request)
  return render_to_response('index.html',c)
  
def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    print("oi")
    if form.is_valid():
      print("oi again")
      form.save()
      return HttpResponseRedirect('/')
  else:
    form = RegisterForm()
  context = {
    'form' : form
  }
  return render(request,'cadastro.html',context)

def ver(request):
  return render(request, 'ver.html',{'tasks':Taskss.objects.all()})

def excluir(request):
  return render(request, 'ver.html',{'tasks':Taskss.objects.all()})

def concluir(request):
  return render(request, 'ver.html',{'tasks':Taskss.objects.all()})

def terminar(request,pk):
  tasks = Taskss.objects.get(id=pk)
  tasks.markup = True
  tasks.save()
  return HttpResponseRedirect('/ver/')

def remover(request,pk):
  tasks = Taskss.objects.get(id=pk)
  tasks.delete()
  return HttpResponseRedirect('/ver/')

class Home(CreateView):
  template_name = 'home.html'
  model = Taskss
  fields = ['user','title','description','markup','begin','end']
  success_url = '/ver'

class WelcomeView(TemplateView):
  def get(self,request):
    template_name = 'index.html'
    form = RegisterForm(request.POST)
    return render(request, template_name)

class Editar(UpdateView):
  model = Taskss
  template_name = 'editar.html'
  form_class = Tasks
  success_url = '/ver'

class Remover(DeleteView):
  model = Taskss
  success_url = '/ver'
  
    

