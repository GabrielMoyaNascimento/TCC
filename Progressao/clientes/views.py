from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from cadastros.models import Categoria, Produto, Pessoa
from .models import Carrinho

class PaginaInicial(TemplateView):
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


class ProdutoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/paginaProduto.html'

class ContatoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/contato.html'


class ConfirmacaoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/confirmacao.html'


class Login(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/login.html'


class Cadastro(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/novaConta.html'



class CadastroCreate( LoginRequiredMixin, CreateView):
    model = Pessoa
    fields = ['nome', 'nascimento', 'email', 'cidade',
              'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
    template_name = 'clientes/novaConta.html'
    success_url = reverse_lazy('clientes-novaConta')
    login_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user

        url = super().form_valid(form)

    # código a fazer depois de salvar objeto no banco
        self.object.atributo = 'usuario'

    # Salva o objeto novamente
        self.object.save()

        return url

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CadastroCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Pessoa"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CadastroUpdate(LoginRequiredMixin, UpdateView):
    model = Pessoa
    fields = ['nome', 'nascimento', 'email', 'cidade',
              'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
    template_name = 'clientes/novaConta.html'
    success_url = reverse_lazy('listar-pessoas')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CadastroUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Pessoa"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user

        url = super().form_valid(form)

    # código a fazer depois de salvar objeto no banco
        self.object.atributo = 'usuario'

    # Salva o objeto novamente
        self.object.save()

        return url

	# Altera a query para buscar o objeto do usuário logado

    def get_object(self, queryset=None):
       self.object = get_object_or_404(
           Pessoa, pk=self.kwargs['pk'], usuario=self.request.user)
       return self.object


# View para adicionar produtos no Carrinho
class AdicionarProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # Também não vai ter template, só colocamos isso porque é obrigatório
    template_name = 'clientes/carrinho.html'

    # Método executado para processar a requisição. É executado antes de renderizar o template
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Recebe a quantidade da url
        qtde = int(kwargs['quantidade'])
        if qtde <= 0:
            return redirect('clientes-carrinho')
            
        # Busca os dados do produto que esta na URL
        prod = get_object_or_404(Produto, pk=kwargs['id_produto'])
       #Se o produto ja estiver no carrinho, ele aumenta a quantidade
        carrinho_tem = False
        carrinho = Carrinho.objects.filter(usuario=self.request.user)
        for c in carrinho:
            if c.produto == prod:
                c.quantidade = c.quantidade + qtde
                c.save()
                carrinho_tem = True
                break


        # Cria um objeto "Carrinho" com os dados do produto e a quantidade da URL
        if carrinho_tem == False:
            carrinho = Carrinho.objects.create(
                quantidade=kwargs['quantidade'],
                produto=prod,
                valor_unid=prod.valorVenda,
                usuario=self.request.user)
        # Redireciona o usuário para a lista
        return redirect('clientes-carrinho')


# View para excluir itens do carrinho
class ExcluirProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # defini qual o modelo pra classe, só pra não bugar
    template_name = "clientes/carrinho.html"
    
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Busca o objeto do carrinho que está na URL
        carrinho = get_object_or_404(Carrinho, pk=kwargs['id_carrinho'])
        # Deleta esse carrinho (objeto)
        carrinho.delete()

        # depois de remover, já redirecina o usuário de novo pra lista
        # Ou seja, o excluir nem tela vai ter... ele vai deletar e voltar pra lista
        return redirect('clientes-carrinho')
    

# View para excluir itens do carrinho
class AtualizarProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # defini qual o modelo pra classe, só pra não bugar
    template_name = "clientes/carrinho.html"
    
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Busca o objeto do carrinho que está na URL
        carrinho = get_object_or_404(Carrinho, pk=kwargs['id_carrinho'])
        # Busca a quantidade nova e transforma pra int
        qtde = int(kwargs['quantidade'])
        
        # Se a quantidade for zero, remove ele, se não atualiza
        if(qtde <= 0):
            carrinho.delete()
        else:
            # Atualiza o objeto, adicionando a qtde na quantidade
            carrinho.quantidade = qtde
            # Salva o objeto
            carrinho.save()

        # depois de remover, já redirecina o usuário de novo pra lista
        # Ou seja, o excluir nem tela vai ter... ele vai deletar e voltar pra lista
        return redirect('clientes-carrinho')
    

# View para listar o carrinho para o usuário
class CarrinhoList(LoginRequiredMixin, ListView):
    model = Carrinho
    template_name = "clientes/carrinho.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        #Pegando valor total dos produtos
        carrinho = Carrinho.objects.filter(usuario=self.request.user)
        total = 0
        for c in carrinho:
            total += c.valor_unid * c.quantidade
        
        # Listar tudo do carrinho desse usuário
        context["carrinho"] = carrinho
        context["valor"] = total

        return context

class ProdutoDetailView(DetailView):
    template_name = "clientes/paginaProduto.html"
    model = Produto
    