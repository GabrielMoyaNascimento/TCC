from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from cadastros.models import Pessoa
from .forms import UsuarioForm

class UsuarioCreate(CreateView):
    form_class = UsuarioForm
    template_name = "clientes/novaConta.html"
    success_url = reverse_lazy("login")

    # Método utilizado para enviar dados ao template
    def get_context_data(self, *args, **kwargs):
        context = super(UsuarioCreate, self).get_context_data(*args, **kwargs)
        context['titulo'] = "Novo Cadastro"
        context['botao'] = "Cadastrar"
        context['classeBotao'] = "btn-success"
        return context

    # Iremos adicionar um grupo ao usuário cadastrado
    def form_valid(self, form):

        # Busca o grupo pelo nome "Usuario"
        # Primeiro faz a busca e depois chama o form valid para inserir o usuário normalmente
        grupo = get_object_or_404(Group, name="Clientes")
    
        # Executa o form_valid padrão... ele vai fazer todas as validações normais
        # Cria o objeto
        url = super().form_valid(form)

        # Se o grupo existir
        if grupo:
            # Adiciona o grupo ao usuário que foi criado nesse form
            self.object.groups.add(grupo)
            # Salva o usuário de novo
            self.object.save()
            # Cria o perfil desse usuário que acabou de se registrar
            pessoa = Pessoa.objects.create(usuario=self.object)

        # Retorno padrão
        return url


class PerfilView(LoginRequiredMixin, DetailView):
    model = Pessoa
    template_name = 'clientes/perfil.html'

    def get_object(self, queryset=None):
       self.object = get_object_or_404(Pessoa, usuario=self.request.user)
       return self.object

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super().get_context_data(*args, **kwargs)

        # context["vendas"] = Venda.objects.filter(usuario=self.request.user)

        return context


class PessoaUpdate(LoginRequiredMixin, UpdateView):
    model = Pessoa
    fields = ['nome', 'nascimento', 'cidade',
              'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
    template_name = 'clientes/novaConta.html'
    success_url = reverse_lazy('clientes-perfil')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super().get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Atualizar meus dados"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


	# Altera a query para buscar o objeto do usuário logado

    def get_object(self, queryset=None):
       self.object = get_object_or_404(Pessoa, usuario=self.request.user)
       return self.object



