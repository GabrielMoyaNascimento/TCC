from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy

#Create View


class PaginaInicial(TemplateView):
    template_name = 'cadastros/index.html'

class EstadoCreate(CreateView):
	model = Estado
	fields = ['sigla', 'nome']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-estados')


class CidadeCreate(CreateView):
	model = Cidade
	fields = ['nome', 'estado']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-cidades')


class PessoaCreate(CreateView):
	model = Pessoa
	fields = ['nome', 'nascimento', 'email', 'cidade',
           'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-pessoas')


class VendaCreate(CreateView):
	model = Venda
	fields = ['data_da_venda', 'valor', 'desconto',
           'parcelas', 'pessoa', 'forma_pagamento']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-vendas')


class ProdutoCreate(CreateView):
	model = Produto
	fields = ['nome', 'codigo', 'descricao', 'estoque',
           'categoria', 'valorVenda']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-produtos')


#class ProdutoVendaCreate(CreateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'forma_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoCreate(CreateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaPagamentos')


class FormaEnvioCreate(CreateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaEnvios')


class CategoriaCreate(CreateView):
	model = Categoria
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-categorias')

#Update View

class EstadoUpdate(UpdateView):
	model = Estado
	fields = ['sigla', 'nome']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-estados')


class CidadeUpdate(UpdateView):
	model = Cidade
	fields = ['nome', 'estado']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-cidades')


class PessoaUpdate(UpdateView):
	model = Pessoa
	fields = ['nome', 'nascimento', 'email', 'cidade',
           'rg', 'cpf', 'endereco', 'cep', 'numero', 'telefone']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-pessoas')


class VendaUpdate(UpdateView):
	model = Venda
	fields = ['data_da_venda', 'valor', 'desconto',
           'parcelas', 'pessoa', 'forma_pagamento']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-vendas')


class ProdutoUpdate(UpdateView):
	model = Produto
	fields = ['nome', 'codigo', 'descricao', 'estoque',
           'categoria', 'valorVenda', 'forma_envio']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-produtos')


#class ProdutoVendaUpdate(UpdateView):
#	model = ProdutoVenda
#	fields = ['produto', 'venda', 'valor_total', 'valor_envio', 'quantidade']
#	template_name = 'cadastros/form.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoUpdate(UpdateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaPagamentos')


class FormaEnvioUpdate(UpdateView):
	model = FormaPagamento
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-formaEnvios')


class CategoriaUpdate(UpdateView):
	model = Categoria
	fields = ['nome', 'descricao']
	template_name = 'cadastros/form.html'
	success_url = reverse_lazy('listar-categorias')

#Delete View


class EstadoDelete(DeleteView):
	model = Estado
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-estados')


class CidadeDelete(DeleteView):
	model = Cidade
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-cidades')


class PessoaDelete(DeleteView):
	model = Pessoa
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-pessoas')


class VendaDelete(DeleteView):
	model = Venda
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-vendas')


class ProdutoDelete(DeleteView):
	model = Produto
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-produtos')


#class ProdutoVendaDelete(DeleteView):
#	model = ProdutoVenda
#	template_name = 'cadastros/formDelete.html'
#	success_url = reverse_lazy('index')


class FormaPagamentoDelete(DeleteView):
	model = FormaPagamento
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-formaPagamentos')

class FormaEnvioDelete(DeleteView):
	model = FormaEnvio
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-formaEnvios')

class CategoriaDelete(DeleteView):
	model = Categoria
	template_name = 'cadastros/formDelete.html'
	success_url = reverse_lazy('listar-categorias')

#List View


class EstadoList(ListView):
	model = Estado
	template_name = 'cadastros/listar_estados.html'


class CidadeList(ListView):
	model = Cidade
	template_name = 'cadastros/listar_cidades.html'

class PessoaList(ListView):
	model = Pessoa
	template_name = 'cadastros/listar_pessoas.html'

class VendaList(ListView):
	model = Venda
	template_name = 'cadastros/listar_vendas.html'

class ProdutoList(ListView):
	model = Produto
	template_name = 'cadastros/listar_produtos.html'

class FormaPagamentoList(ListView):
	model = FormaPagamento
	template_name = 'cadastros/listar_formaPagamentos.html'

class FormaEnvioList(ListView):
	model = FormaEnvio
	template_name = 'cadastros/listar_formaEnvios.html'

class CategoriaList(ListView):
	model = Categoria
	template_name = 'cadastros/listar_categorias.html'

