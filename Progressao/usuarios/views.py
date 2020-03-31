from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView

class UsuarioCreate(CreateView):
    form_class = UserCreationForm
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

        # Retorno padrão
        return url
