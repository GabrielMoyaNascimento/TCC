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



class CarrinhoCreate (LoginRequiredMixin, CreateView):
    # defini qual o modelo pra classe
    model = Carrinho
    template_name = "clientes/carrinho.html"

    # Pra onde redirecionar o usuario  depois de inserir
    success_url = reverse_lazy("adicionar-produto")
    # quais campos vai aparecer no formulario
    fields = ['quantidade','valor_unid','produto', 'usuario']

    # Valida o formulário e salva no banco
    def form_valid(self, form):

        # Recebe os dados do formulário
        quantidade = form.cleaned_data['quantidade']
        produto = form.cleaned_data['produto']

        # Verificar se o estoque do produto é maior que a quantidade
        if(int(produto.estoque) < int(quantidade)):

            # Pode fazer o procedimento padrão
            form.add_error(None, 'A quantidade informada não tem no estoque.')

            # Chamar o super
            return self.form_invalid(form)
        # se ok
        else:    
            return super().form_valid(form)



    def get_context_data(self, *args, **kwargs):
        context = super( CarrinhoCreate, self).get_context_data(*args, **kwargs)


        context['titulo'] = "Adicionar produto no Carrinho"
        context['botao'] = "Adicionar"
        context['classbotao'] = "btn-success"
        context['urlvoltar'] = "clientes-carrinho"

        return context


class CarrinhoUpdate (LoginRequiredMixin, UpdateView):
    # defini qual o modelo pra classe

    model = Carrinho
    template_name = "clientes/carrinho.html"

    # Pra onde redirecionar o usuario  depois de inserir
    success_url = reverse_lazy("clientes-carrinho")
    # quais campos vai aparecer no formulario
    fields = ['quantidade','valor_unid','produto', 'usuario']

    def get_context_data(self, *args, **kwargs):
        context = super(CarrinhoUpdate, self).get_context_data(*args, **kwargs)

        # adiciona coisas ao contextos das coisas
        context['titulo'] = "Atualizar carrinho"
        context['botao'] = "Atualizar"
        context['classbotao'] = "btn-success"
        context['urlvoltar'] = "clientes-carrinho"

        return context


class CarrinhoDelete(LoginRequiredMixin, DeleteView):
    # defini qual o modelo pra classe

    model = Carrinho
    template_name = "clientes/carrinho.html"
    # Pra onde redirecionar o usuario  depois de inserir
    success_url = reverse_lazy("lista-vender-produtos")
    # quais campos vai aparecer no formulario

    def get_context_data(self, *args, **kwargs):
        context = super(CarrinhoDelete, self).get_context_data(*args, **kwargs)

        # adiciona coisas ao contextos das coisas
        context['titulo'] = "Remover do Carrinho"
        context['botao'] = "Remover"
        context['classbotao'] = "btn-danger"
        context['urlvoltar'] = "clientes-carrinho"

        return context

class CarrinhoList(LoginRequiredMixin, ListView):
    model = Carrinho
    template_name = "clientes/carrinho.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Listar tudo do carrinho desse usuário
        context["carrinho"] = Carrinho.objects.filter(usuario=self.request.user)
        return context