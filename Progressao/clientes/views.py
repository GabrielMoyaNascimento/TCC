from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from cadastros.models import Categoria, Produto
from .models import Carrinho

class PaginaInicial(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Filtra a categoria
        cat = self.request.GET.get('categoria')  # Recebe a página atual
        # Se existir, filta pelo nome da categoria
        if cat:
            produtos = Produto.objects.filter(
                categoria__nome=cat).reverse()  # [0:9]
        # se não, busca todos
        else:
            # [0:9] # Busca os produtos
            produtos = Produto.objects.all().reverse()

        paginator = Paginator(produtos, 9)  # Divide os produtos em páginas
        page = self.request.GET.get('pagina')  # Recebe a página atual
        produtos = paginator.get_page(page)  # Filtra os produtos dessa página
        context['produtos'] = produtos

        context['categorias'] = Categoria.objects.all()
        return context


class CarrinhoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/carrinho.html'


class Login(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/login.html'


class Cadastro(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/novaConta.html'


class AdicionarCarrinho(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/carrinho.html'

    # Método executado para processar a requisição. É executado antes de renderizar o template
    def dispatch(self, *args, **kwargs):

        # Busca os dados do produto que esta na URL
        prod = get_object_or_404(Produto, pk=kwargs['id_produto'])

        # Cria um objeto "Carrinho" com os dados do produto e a quantidade da URL
        carrinho = Carrinho.objects.create(
            quantidade=kwargs['quantidade'],
            produto=prod,
            valor_unid=prod.valorVenda,
            usuario=self.request.user)

        return super().dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Listar tudo do carrinho desse usuário
        context["carrinho"] = Carrinho.objects.filter(usuario=self.request.user)
        return context


