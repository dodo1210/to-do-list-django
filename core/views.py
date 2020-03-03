from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from .models import Tasks as Taskss
from .models import MainTasks as MainTaskss
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.core.mail import send_mail
from datetime import datetime,timezone
from fpdf import FPDF
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def auth_view(request):
  user  = auth.authenticate(username=request.POST.get('username',''), password=request.POST.get('password',''))
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
      user = User.objects.all().last()
      token = Token.objects.create(user=user)
      return HttpResponseRedirect('/')
  else:
    form = RegisterForm()
  context = {
    'form' : form
  }
  return render(request,'cadastro.html',context)

def change_password(request,pk):
  user = User.objects.get(id=pk)
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)
    if form.is_valid():
      form.save()
      update_session_auth_hash(request, user)
      return HttpResponseRedirect('/') 
    else:
      return HttpResponseRedirect('/mudar_senha/'+str(pk))
  else:
    form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'mudar_senha.html', args)

def ver(request):
  return render(request, 'ver.html',{'tasks':MainTaskss.objects.all()})

def prioridades(request,pk):
  tasks = Taskss.objects.filter(main_task=MainTaskss.objects.get(id=pk))
  date = []
  count = 0
  for t in tasks:
    if t.markup == False:
      date.append(str(t.end))
    elif str(t.begin).split('-')[2].split(' ')[0] == str(datetime.now()).split('-')[2].split(' ')[0]:
      date.append(str(t.markup_end))
  date_sort = []
  for d in sorted(date): 
    date_sort.append(d)
  email(request,date_sort)
  return HttpResponseRedirect('/ver_tarefa/'+str(pk)) 

def email(request,date_sort):
  tasks = Taskss.objects.all()
  tarefa = 'As tarefas finalizadas hoje são as primeiras: \n'

  for d in date_sort:
    for t in tasks:
      if str(t.end) == str(d):
        tarefa+=' '+t.title+' que finaliza '+str(t.end)+'\n'
        break
      elif d.split('-')[2].split(' ')[0] == str(datetime.now()).split('-')[2].split(' ')[0] and t.markup == True:
        tarefa+=' '+t.title+' foi finalizada hoje '+str(t.markup_end)+'\n'
        break

  """pdf = FPDF()
        pdf.set_font("Arial", size=12)
        pdf.add_page()
        for t in tarefa.split('\n'):
          pdf.cell(0, 10, txt=t, ln=10, align="L") 
        pdf.output("multipage_simple.pdf")"""

  subject = request.POST.get('subject', 'FINALIZAÇÃO DE TAREFA')
  message = request.POST.get('message', tarefa)
  
  from_email = request.POST.get('from_email', 'contatoiatrader@gmail.com')
  if subject and message and from_email:
    try:
      send_mail(subject, message, from_email, ['contatodouglassiqueira@gmail.com'])
      return JsonResponse({"email":"Relatório saindo"})
    except BadHeaderError:
      return JsonResponse({"email":'Não foi possível enviar email'})

def terminar(request,pk):
  tasks = Taskss.objects.get(id=pk)
  tasks.markup_end = datetime.now()
  tasks.markup = True
  tasks.save()
  return HttpResponseRedirect('/ver_tarefa/'+str(tasks.main_task.pk))

def sub_task(request,pk):
  m_task = MainTaskss.objects.get(id=pk)
  form = Tasks(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      task = form.save(commit=False)
      id = []
      for i in str(request.POST).split('\''):
        try:
          id.append(int(i))
        except:
          pass
      print("oi")
      task.begin = datetime.now()
      task.main_task = m_task
      user = request.POST.get('user','')
      task.save()
      task.user.add(*id)
      return HttpResponseRedirect('/ver/')
  return render(request,'sub_tarefas.html',{'form':form,'pk':pk})

def view_sub_task(request,pk):
  return render(request, 'ver_sub.html',{'tasks':Taskss.objects.filter(main_task = MainTaskss.objects.get(id=pk)),'pk':pk})  

def date_interview(request,pk,date):
  begin_end = date.split('_')
  tasks = Taskss.objects.filter(main_task=MainTaskss.objects.get(id=pk))
  begin = []
  end = []
  b = begin_end[0]+" 00:00:00.000000"
  e = begin_end[1]+" 23:59:59"

  for t in tasks:
    if datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f") <= datetime.strptime(str(t.begin).split('+')[0], "%Y-%m-%d %H:%M:%S.%f"):
      begin.append(t.pk)

  for t in tasks:
    if datetime.strptime(e, "%Y-%m-%d %H:%M:%S") > datetime.strptime(str(t.end).split('+')[0], "%Y-%m-%d %H:%M:%S"):
      end.append(t.pk)

  date_sort = []
  for b in begin:
    for e in end:
      if b==e:
        t = Taskss.objects.get(id = b)
        date_sort.append(str(t.end))
        break
  if date_sort == []:
    return JsonResponse({"email":'Não foi possível enviar email, pois não há tarefas'})
  a = email(request,date_sort)
  if str(a) == '<JsonResponse status_code=200, "application/json">':
    return JsonResponse({"email":'Email enviado com sucesso'})
  else:
    return JsonResponse({"email":'Não foi possível enviar email'})

def remover_tarefa(request,pk):
  tasks = Taskss.objects.get(id=pk)
  tasks.delete()
  return HttpResponseRedirect('/ver/')

def remover(request,pk):
  tasks = MainTaskss.objects.get(id=pk)
  tasks.delete()
  return HttpResponseRedirect('/ver/')

class Home(CreateView):
  template_name = 'home.html'
  model = MainTaskss
  fields = ['title']
  success_url = '/ver/'

class Tarefas(CreateView):
  template_name = 'home.html'
  model = Taskss
  fields = ['user','title','end']
  def get_success_url(self,request,**kwargs):
    return reverse('notes_detail',kwargs={'pk':self.object.pk})

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
  model = MainTaskss
  template_name = 'editar.html'
  form_class = MainTasks
  success_url = '/ver/'

class EditarTarefa(UpdateView):
  model = Taskss
  template_name = 'editar.html'
  form_class = Tasks
  success_url = '/ver/'


