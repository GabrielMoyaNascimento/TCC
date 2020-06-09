from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import *
from datetime import datetime
from django.db.models import Sum

# Create View


class PaginaInicial(GroupRequiredMixin,LoginRequiredMixin, TemplateView):
    template_name = 'cadastros/index.html'
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        #Filtro de vendas por data
        dmin = self.request.GET.get('min_date')
        dmax = self.request.GET.get('max_date')
        if dmin is not None and dmax is not None:
            
            lista = Venda.objects.filter(data_da_venda__range=(dmin, dmax))
            context['valorTotal'] = lista.aggregate(Sum('valor'))
            context['lista'] = lista
            context['estoque'] = Produto.objects.filter(estoque__range=(-10, 3)).count()
            context['produto'] = Produto.objects.all().count()
            context['venda'] = Venda.objects.all().count()
        return context


class PaginaCliente(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'cadastros/exemploTelaCliente.html'
    group_required = u"Administrador"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
       
        # Filtra a categoria
        cat = self.request.GET.get('categoria')  # Recebe a página atual
        # Se existir, filta pelo nome da categoria
        if cat:
            produtos = Produto.objects.filter(categoria__nome=cat).reverse()  # [0:9]
        # se não, busca todos
        else:
            produtos = Produto.objects.all().reverse()  # [0:9] # Busca os produtos

        paginator = Paginator(produtos, 9) # Divide os produtos em páginas
        page = self.request.GET.get('pagina')  # Recebe a página atual
        produtos = paginator.get_page(page) # Filtra os produtos dessa página
        context['produtos'] = produtos

        context['categorias'] = Categoria.objects.all()
        return context


class EstadoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Estado
    fields = ['sigla', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(EstadoCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de novo Estado"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CidadeCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Cidade
    fields = ['nome', 'estado']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cidades')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CidadeCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Cidade"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

        # Devolve/envia o context para seu comportamento padrão
        return context



class ProdutoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome', 'codigo', 'descricao', 'estoque',
              'categoria', 'valorVenda', 'imagem']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-produtos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(ProdutoCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de novo Produto"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class EntradaProdutoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = EntradaProduto
    fields = ['produto', 'quantidade']
    template_name = 'cadastros/form_confirmacao.html'
    success_url = reverse_lazy('listar-entrada-produtos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def form_valid(self, form):
        url = super().form_valid(form)
        self.object.produto
        self.object.produto.estoque += self.object.quantidade
        self.object.produto.save()
        return url

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super().get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro Entrada de Produto"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class FormaPagamentoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = FormaPagamento
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaPagamentos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaPagamentoCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Forma de Pagamento"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class FormaEnvioCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = FormaEnvio
    fields = ['nome', 'descricao', 'valor']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaEnvios')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaEnvioCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Forma de Envio"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CategoriaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-categorias')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CategoriaCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Categoria"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CupomCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Cupom
    fields = ['nome', 'desconto', 'validade']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cupons')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CupomCreate, self).get_context_data(
            *args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de novo Cupom"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context



# Update View

class EstadoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Estado
    fields = ['sigla', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"



    
    
    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(EstadoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Estado"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CidadeUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Cidade
    fields = ['nome', 'estado']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cidades')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"




    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CidadeUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Cidade"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context

class ProdutoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'codigo', 'descricao',
              'categoria', 'valorVenda', 'imagem']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-produtos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(ProdutoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Produto"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class FormaPagamentoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = FormaPagamento
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaPagamentos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"




    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaPagamentoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Forma de Pagamento"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class FormaEnvioUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = FormaEnvio
    fields = ['nome', 'descricao', 'valor']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaEnvios')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"



    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaEnvioUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Forma de Envio"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CategoriaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-categorias')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CategoriaUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Categoria"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CupomUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Cupom
    fields = ['nome', 'desconto', 'validade']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cupons')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CupomUpdate, self).get_context_data(
            *args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Cupom"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context




# Delete View
class EstadoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Estado
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


class CidadeDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Cidade
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-cidades')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

class ProdutoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-produtos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

class FormaPagamentoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = FormaPagamento
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-formaPagamentos')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


class FormaEnvioDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = FormaEnvio
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-formaEnvios')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


class CategoriaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-categorias')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


class CupomDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Cupom
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-cupons')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


# List View
class EstadoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Estado
    template_name = 'cadastros/listar_estados.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        
        estados = Estado.objects.all().reverse()
        # paginator = Paginator(estados, 5)  # Divide os estados em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # estados = paginator.get_page(page)  # Filtra os estados dessa página
        context['estados'] = estados
        return context


class CidadeList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Cidade
    template_name = 'cadastros/listar_cidades.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        cidades = Cidade.objects.all().reverse()

        # paginator = Paginator(cidades, 5)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # cidades = paginator.get_page(page)  # Filtra os objetos dessa página
        context['cidades'] = cidades
        return context


class PessoaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Pessoa
    template_name = 'cadastros/listar_pessoas.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

   
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        pessoas = Pessoa.objects.all().reverse()

        # paginator = Paginator(pessoas, 10)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # pessoas = paginator.get_page(page)  # Filtra os objetos dessa página
        context['pessoas'] = pessoas
        return context


class VendaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'cadastros/listar_vendas.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        vendas = Venda.objects.all()

        # paginator = Paginator(vendas, 10)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # vendas = paginator.get_page(page)  # Filtra os objetos dessa página
        context['vendas'] = vendas
        return context


class ProdutoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'cadastros/listar_produtos.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        produtos = Produto.objects.all().reverse()

        paginator = Paginator(produtos, 10)  # Divide  em páginas
        page = self.request.GET.get('pagina')  # Recebe a página atual
        produtos = paginator.get_page(page)  # Filtra os objetos dessa página
        context['produtos'] = produtos
        return context


class EntradaProdutoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = EntradaProduto
    template_name = 'cadastros/listar_entrada_produtos.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        entrada = EntradaProduto.objects.all().reverse()

        # paginator = Paginator(entrada, 10)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # entrada = paginator.get_page(page)  # Filtra os objetos dessa página
        context['entrada'] = entrada
        return context

class BaixoEstoqueProdutoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'cadastros/listar_baixo_estoque.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        baixo = Produto.objects.filter(estoque__range=(-10, 3))
        # paginator = Paginator(entrada, 10)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # entrada = paginator.get_page(page)  # Filtra os objetos dessa página
        context['baixo'] = baixo
        return context
    

class FormaPagamentoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = FormaPagamento
    template_name = 'cadastros/listar_formaPagamentos.html'
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        pagamentos = FormaPagamento.objects.all().reverse()

        # paginator = Paginator(pagamentos, 5)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # pagamentos = paginator.get_page(page)  # Filtra os objetos dessa página
        context['pagamentos'] = pagamentos
        return context


class FormaEnvioList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = FormaEnvio
    template_name = 'cadastros/listar_formaEnvios.html'
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        envios = FormaEnvio.objects.all().reverse()

        # paginator = Paginator(envios, 5)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # envios = paginator.get_page(page)  # Filtra os objetos dessa página
        context['envios'] = envios
        return context


class CategoriaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'cadastros/listar_categorias.html'
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        categorias = Categoria.objects.all().reverse()

        # paginator = Paginator(categorias, 5)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # categorias = paginator.get_page(page)  # Filtra os objetos dessa página
        context['categorias'] = categorias
        return context


class CupomList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Cupom
    template_name = 'cadastros/listar_cupons.html'
    group_required = u"Administrador"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        cupons = Cupom.objects.all().reverse()

        # paginator = Paginator(cupons, 5)  # Divide  em páginas
        # page = self.request.GET.get('pagina')  # Recebe a página atual
        # cupons = paginator.get_page(page)  # Filtra os objetos dessa página
        context['cupons'] = cupons
        return context
