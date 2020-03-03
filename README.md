# to do list django

Esta aplicação cria-se lista com nomes e sub tarefas para cada lista. Além disso, é enviado para o email com uma lista de prioridades. Também há a possibilidade de gerar relatórios do momento em que esta as tarefas.

/mudar_senha/id -> Página para mudança de senha após a verificação.
/register -> cadastro de usuário

/remover/id -> Remove tarefa a tarefa principal.

ver/ -> Lista de todas as tarefas

/sub_tarefa/id -> Cadastro das lista de tarefa (sub tarefas). É necessário a ID da tarefa.

/ver_tarefa/id -> Verifica as lista de tarefas (sub tarefas). É necessário a ID da tarefa.

/terminar/id -> Finaliza a tarefa, ou sub tarefas.

/datas/id/datainicial_datafinal -> Esta parte não contém interface e contém em background o envio de email dentro de um intervalo de datas. Para executar deve ser usado a id da tarefa principal e separar em barra, que indica a data inicial e a final. Para enviar as datas deve ser separado por uma underline. EX: 2020-03-01_2020-03-03. Foi utilizado o Postman nesta url

/remover_tarefa/id -> Remove a subtarefa ou uma das lista de tarefa.

/editar_tarefa/id -> Edita uma das opções da lista de tarefa

/editar/id -> Edita a tarefa principal

/verificar_usuario -> Opção prévia a troca de senha

/home/ -> Página principal após a autenticação, na mesma pode ser criada uma tarefa

/ -> Tela de login

Contém um usuário criado com nome: biome, email:admin@biome-hub.com e senha 040632
