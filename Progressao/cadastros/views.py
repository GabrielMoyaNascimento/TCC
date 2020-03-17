from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .models import *


#Create View


class PaginaInicial(LoginRequiredMixin,TemplateView):
    template_name = 'cadastros/index.html'
	

class EstadoCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = Estado
	fields = ['sigla', 'nome']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-estados')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"


class CidadeCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = Cidade
	fields = ['nome', 'estado']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-cidades')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"


class PessoaCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = Pessoa
	fields = ['nome', 'nascimento', 'email', 'cidade',
           'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-pessoas')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"


class VendaCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = Venda
	fields = ['data_da_venda', 'valor', 'desconto',
           'parcelas', 'pessoa', 'forma_pagamento']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-vendas')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"


class ProdutoCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = Produto
	fields = ['nome', 'codigo', 'descricao', 'estoque',
           'categoria', 'valorVenda']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-produtos')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"

#class ProdutoVendaCreate(CreateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'forma_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaPagamentos')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"


class FormaEnvioCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
	model = FormaEnvio
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaEnvios')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"

class CategoriaCreate(GroupRequiredMixin,LoginRequiredMixin,CreateView):
	model = Categoria
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-categorias')
	login_url = reverse_lazy('login')
	group_required = u"Administrador"

#Update View


class EstadoUpdate(LoginRequiredMixin,UpdateView):
	model = Estado
	fields = ['sigla', 'nome']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-estados')
	login_url = reverse_lazy('login')

class CidadeUpdate(LoginRequiredMixin,UpdateView):
	model = Cidade
	fields = ['nome', 'estado']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-cidades')
	login_url = reverse_lazy('login')

class PessoaUpdate(LoginRequiredMixin,UpdateView):
	model = Pessoa
	fields = ['nome', 'nascimento', 'email', 'cidade',
           'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-pessoas')
	login_url = reverse_lazy('login')

class VendaUpdate(LoginRequiredMixin,UpdateView):
	model = Venda
	fields = ['data_da_venda', 'valor', 'desconto',
           'parcelas', 'pessoa', 'forma_pagamento']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-vendas')
	login_url = reverse_lazy('login')

class ProdutoUpdate(LoginRequiredMixin,UpdateView):
	model = Produto
	fields = ['nome', 'codigo', 'descricao', 'estoque',
           'categoria', 'valorVenda', 'forma_envio']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-produtos')
	login_url = reverse_lazy('login')

#class ProdutoVendaUpdate(UpdateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'valor_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoUpdate(LoginRequiredMixin,UpdateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaPagamentos')
	login_url = reverse_lazy('login')

class FormaEnvioUpdate(LoginRequiredMixin,UpdateView):
	model = FormaEnvio
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaEnvios')
	login_url = reverse_lazy('login')

class CategoriaUpdate(LoginRequiredMixin,UpdateView):
	model = Categoria
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-categorias')
	login_url = reverse_lazy('login')
#Delete View


class EstadoDelete(LoginRequiredMixin,DeleteView):
	model = Estado
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-estados')
	login_url = reverse_lazy('login')

class CidadeDelete(LoginRequiredMixin,DeleteView):
	model = Cidade
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-cidades')
	login_url = reverse_lazy('login')

class PessoaDelete(LoginRequiredMixin,DeleteView):
	model = Pessoa
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-pessoas')
	login_url = reverse_lazy('login')

class VendaDelete(LoginRequiredMixin,DeleteView):
	model = Venda
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-vendas')


class ProdutoDelete(LoginRequiredMixin,DeleteView):
	model = Produto
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-produtos')
	login_url = reverse_lazy('login')

#class ProdutoVendaDelete(DeleteView):
#	model = ProdutoVenda
#	template_name = 'cadastros/formDelete.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoDelete(LoginRequiredMixin,DeleteView):
	model = FormaPagamento
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-formaPagamentos')
	login_url = reverse_lazy('login')

class FormaEnvioDelete(LoginRequiredMixin,DeleteView):
	model = FormaEnvio
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-formaEnvios')
	login_url = reverse_lazy('login')

class CategoriaDelete(LoginRequiredMixin,DeleteView):
	model = Categoria
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-categorias')
	login_url = reverse_lazy('login')
#List View


class EstadoList(LoginRequiredMixin,ListView):
	model = Estado
	template_name = 'cadastros/listar_estados.html'
	login_url = reverse_lazy('login')

class CidadeList(LoginRequiredMixin,ListView):
	model = Cidade
	template_name = 'cadastros/listar_cidades.html'
	login_url = reverse_lazy('login')
	login_url = reverse_lazy('login')
class PessoaList(LoginRequiredMixin,ListView):
	model = Pessoa
	template_name = 'cadastros/listar_pessoas.html'
	login_url = reverse_lazy('login')

class VendaList(LoginRequiredMixin,ListView):
	model = Venda
	template_name = 'cadastros/listar_vendas.html'
	login_url = reverse_lazy('login')

class ProdutoList(LoginRequiredMixin,ListView):
	model = Produto
	template_name = 'cadastros/listar_produtos.html'
	login_url = reverse_lazy('login')

class FormaPagamentoList(LoginRequiredMixin,ListView):
	model = FormaPagamento
	template_name = 'cadastros/listar_formaPagamentos.html'
	login_url = reverse_lazy('login')

class FormaEnvioList(LoginRequiredMixin,ListView):
	model = FormaEnvio
	template_name = 'cadastros/listar_formaEnvios.html'


class CategoriaList(LoginRequiredMixin,ListView):
	model = Categoria
	template_name = 'cadastros/listar_categorias.html'

