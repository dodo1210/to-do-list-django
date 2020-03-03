from __future__ import absolute_import
from celery import shared_task
from relatorios import gerar_relatorio_excel

@shared_task
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