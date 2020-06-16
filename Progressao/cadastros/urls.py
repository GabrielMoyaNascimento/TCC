from django.urls import path
# Importa as views que a gente criou 
from .views import *
from clientes.views import VendaCreate
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    #Index e exemplo da tela de clientes
    path('adm/', PaginaInicial.as_view(), name="cadastrar-index"),
    path('adm/exemplo', PaginaCliente.as_view(), name="exemplo-cliente"),

    # Create View
    path('adm/cadastrar/estado/', EstadoCreate.as_view(), name="cadastrar-estado"),
    path('adm/cadastrar/cidade/', CidadeCreate.as_view(), name="cadastrar-cidade"),
    path('adm/cadastrar/produto/', ProdutoCreate.as_view(), name="cadastrar-produto"),
    path('adm/cadastrar/categoria/', CategoriaCreate.as_view(), name="cadastrar-categoria"),
    path('adm/cadastrar/formaPagamento/', FormaPagamentoCreate.as_view(), name="cadastrar-formaPagamento"),
    path('adm/cadastrar/formaPagamento/', FormaPagamentoCreate.as_view(), name="cadastrar-formaPagamento"),
    path('adm/cadastrar/formaEnvio/', FormaEnvioCreate.as_view(),name="cadastrar-formaEnvio"),
    path('adm/cadastrar/cupom/', CupomCreate.as_view(), name="cadastrar-cupom"),
    path('adm/cadastrar/entradaProduto/', EntradaProdutoCreate.as_view(), name="entrada-produto"),

    
    #Update View
    path('adm/atualizar/estado/<int:pk>/',EstadoUpdate.as_view(), name="atualizar-estado"),
    path('adm/atualizar/cidade/<int:pk>/',CidadeUpdate.as_view(), name="atualizar-cidade"),
    path('adm/atualizar/produto/<int:pk>/',ProdutoUpdate.as_view(), name="atualizar-produto"),
    path('adm/atualizar/categoria/<int:pk>/',CategoriaUpdate.as_view(), name="atualizar-categoria"),
    path('adm/atualizar/formaPagamento/<int:pk>/',FormaPagamentoUpdate.as_view(), name="atualizar-formaPagamento"),
    path('adm/atualizar/formaEnvio/<int:pk>/',FormaEnvioUpdate.as_view(), name="atualizar-formaEnvio"),
    path('adm/atualizar/cupom/<int:pk>/',CupomUpdate.as_view(), name="atualizar-cupom"),


    #Delete View
    path('adm/excluir/estado/<int:pk>/', EstadoDelete.as_view(), name="deletar-estado"),
    path('adm/excluir/cidade/<int:pk>/', CidadeDelete.as_view(), name="deletar-cidade"),
    path('adm/excluir/produto/<int:pk>/', ProdutoDelete.as_view(), name="deletar-produto"),
    path('adm/excluir/categoria/<int:pk>/', CategoriaDelete.as_view(), name="deletar-categoria"),
    path('adm/excluir/formaPagamento/<int:pk>/', FormaPagamentoDelete.as_view(), name="deletar-formaPagamento"),
    path('adm/excluir/formaEnvio/<int:pk>/', FormaEnvioDelete.as_view(), name="deletar-formaEnvio"),
    path('adm/excluir/cupom/<int:pk>/', CupomDelete.as_view(), name="deletar-cupom"),



    #List View
    path('adm/listar/estados/', EstadoList.as_view(), name="listar-estados"),
    path('adm/listar/cidades/', CidadeList.as_view(), name="listar-cidades"),
    path('adm/listar/pessoas/', PessoaList.as_view(), name="listar-pessoas"),
    path('adm/listar/produtos/', ProdutoList.as_view(), name="listar-produtos"),
    path('adm/listar/categorias/', CategoriaList.as_view(), name="listar-categorias"),
    path('adm/listar/formaPagamentos/', FormaPagamentoList.as_view(), name="listar-formaPagamentos"),
    path('adm/listar/formaEnvios/', FormaEnvioList.as_view(), name="listar-formaEnvios"),
    path('adm/listar/vendas/', VendaList.as_view(), name="listar-vendas"),
    path('adm/listar/cupons/', CupomList.as_view(), name="listar-cupons"),
    path('adm/listar/entradas/', EntradaProdutoList.as_view(), name="listar-entrada-produtos"),
    path('adm/listar/parcelas/', ParcelaList.as_view(), name="listar-parcelas"),
    path('adm/listar/baixoEstoque/', BaixoEstoqueProdutoList.as_view(), name="listar-baixo-estoque-produtos"),

]
