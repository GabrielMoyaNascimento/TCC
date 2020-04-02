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


# Create View


class PaginaInicial(GroupRequiredMixin,LoginRequiredMixin, TemplateView):
    template_name = 'cadastros/index.html'
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

class EstadoCreate(LoginRequiredMixin, CreateView):
    model = Estado
    fields = ['sigla', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')
    

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


class PessoaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Pessoa
    fields = ['nome', 'nascimento', 'email', 'cidade',
              'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-pessoas')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"


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
        context = super(PessoaCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Pessoa"
        context['botao'] = "Cadastrar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class VendaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Venda
    fields = ['data_da_venda', 'valor', 'desconto',
              'parcelas', 'pessoa', 'forma_pagamento']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-vendas')
    login_url = reverse_lazy('login')
    group_required = u"Administrador"

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
        context = super(VendaCreate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Cadastro de nova Venda"
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

# class ProdutoVendaCreate(CreateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'forma_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')


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
    fields = ['nome', 'descricao']
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

# Update View


class EstadoUpdate(LoginRequiredMixin, UpdateView):
    model = Estado
    fields = ['sigla', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(EstadoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Estado"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CidadeUpdate(LoginRequiredMixin, UpdateView):
    model = Cidade
    fields = ['nome', 'estado']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cidades')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CidadeUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Cidade"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class VendaUpdate(LoginRequiredMixin, UpdateView):
    model = Venda
    fields = ['data_da_venda', 'valor', 'desconto',
              'parcelas', 'pessoa', 'forma_pagamento']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-vendas')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(VendaUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Venda"
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
       self.object = get_object_or_404(Pessoa, pk=self.kwargs['pk'], usuario=self.request.user)
       return self.object


class ProdutoUpdate(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'codigo', 'descricao', 'estoque',
              'categoria', 'valorVenda', 'imagem']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-produtos')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(ProdutoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Produto"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context

# class ProdutoVendaUpdate(UpdateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'valor_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')



class FormaPagamentoUpdate(LoginRequiredMixin, UpdateView):
    model = FormaPagamento
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaPagamentos')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaPagamentoUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Forma de Pagamento"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class FormaEnvioUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEnvio
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-formaEnvios')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(FormaEnvioUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Forma de Envio"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context


class CategoriaUpdate(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-categorias')
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(CategoriaUpdate, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Update de Categoria"
        context['botao'] = "Salvar"
        context['classe'] = "btn-success"

    # Devolve/envia o context para seu comportamento padrão
        return context





# Delete View
class EstadoDelete(LoginRequiredMixin, DeleteView):
    model = Estado
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-estados')
    login_url = reverse_lazy('login')


class CidadeDelete(LoginRequiredMixin, DeleteView):
    model = Cidade
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-cidades')
    login_url = reverse_lazy('login')


class VendaDelete(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-vendas')

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
       self.object = get_object_or_404(Venda, pk=self.kwargs['pk'], usuario=self.request.user)
       return self.object


class ProdutoDelete(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-produtos')
    login_url = reverse_lazy('login')

# class ProdutoVendaDelete(DeleteView):
#	model = ProdutoVenda
#	template_name = 'cadastros/formDelete.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoDelete(LoginRequiredMixin, DeleteView):
    model = FormaPagamento
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-formaPagamentos')
    login_url = reverse_lazy('login')


class FormaEnvioDelete(LoginRequiredMixin, DeleteView):
    model = FormaEnvio
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-formaEnvios')
    login_url = reverse_lazy('login')


class CategoriaDelete(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'cadastros/formDelete.html'
    success_url = reverse_lazy('listar-categorias')
    login_url = reverse_lazy('login')
# List View


class EstadoList(LoginRequiredMixin, ListView):
    model = Estado
    template_name = 'cadastros/listar_estados.html'
    login_url = reverse_lazy('login')


class CidadeList(LoginRequiredMixin, ListView):
    model = Cidade
    template_name = 'cadastros/listar_cidades.html'
    login_url = reverse_lazy('login')
    login_url = reverse_lazy('login')


class PessoaList(LoginRequiredMixin, ListView):
    model = Pessoa
    template_name = 'cadastros/listar_pessoas.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Pessoa.objects.all()
        return self.object_list


class VendaList(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'cadastros/listar_vendas.html'
    login_url = reverse_lazy('login')


    def get_queryset(self):
       # O object_list armazena uma lista de objetos de um ListView
       self.object_list = Venda.objects.filter(usuario=self.request.user)
       return self.object_list

class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'cadastros/listar_produtos.html'
    login_url = reverse_lazy('login')
    
    

class FormaPagamentoList(LoginRequiredMixin, ListView):
    model = FormaPagamento
    template_name = 'cadastros/listar_formaPagamentos.html'
    login_url = reverse_lazy('login')


class FormaEnvioList(LoginRequiredMixin, ListView):
    model = FormaEnvio
    template_name = 'cadastros/listar_formaEnvios.html'


class CategoriaList(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'cadastros/listar_categorias.html'
