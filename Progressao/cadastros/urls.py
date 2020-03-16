from django.urls import path
# Importa as views que a gente criou 
from .views import *
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    # Create View
    path('cadastrar/index/', PaginaInicial.as_view(), name="cadastrar-index"),
    path('cadastrar/estado/', EstadoCreate.as_view(), name="cadastrar-estado"),
    path('cadastrar/cidade/', CidadeCreate.as_view(), name="cadastrar-cidade"),
    path('cadastrar/pessoa/', PessoaCreate.as_view(), name="cadastrar-pessoa"),
    path('cadastrar/produto/', ProdutoCreate.as_view(), name="cadastrar-produto"),
    path('cadastrar/categoria/', CategoriaCreate.as_view(), name="cadastrar-categoria"),
    path('cadastrar/formaPagamento/', FormaPagamentoCreate.as_view(), name="cadastrar-formaPagamento"),
    path('cadastrar/formaEnvio/', FormaEnvioCreate.as_view(),name="cadastrar-formaEnvio"),
    path('cadastrar/venda/', VendaCreate.as_view(), name="cadastrar-venda"),
    
    #Update View
    path('atualizar/estado/<int:pk>/',EstadoUpdate.as_view(), name="atualizar-estado"),
    path('atualizar/cidade/<int:pk>/',CidadeUpdate.as_view(), name="atualizar-cidade"),
    path('atualizar/pessoa/<int:pk>/',PessoaUpdate.as_view(), name="atualizar-pessoa"),
    path('atualizar/produto/<int:pk>/',ProdutoUpdate.as_view(), name="atualizar-produto"),
    path('atualizar/categoria/<int:pk>/',CategoriaUpdate.as_view(), name="atualizar-categoria"),
    path('atualizar/formaPagamento/<int:pk>/',FormaPagamentoUpdate.as_view(), name="atualizar-formaPagamento"),
    path('atualizar/formaEnvio/<int:pk>/',FormaEnvioUpdate.as_view(), name="atualizar-formaEnvio"),
    path('atualizar/venda/<int:pk>/',VendaUpdate.as_view(), name="atualizar-venda"),

    #Delete View
    path('excluir/estado/<int:pk>/', EstadoDelete.as_view(), name="deletar-estado"),
    path('excluir/cidade/<int:pk>/', CidadeDelete.as_view(), name="deletar-cidade"),
    path('excluir/pessoa/<int:pk>/', PessoaDelete.as_view(), name="deletar-pessoa"),
    path('excluir/produto/<int:pk>/', ProdutoDelete.as_view(), name="deletar-produto"),
    path('excluir/categoria/<int:pk>/', CategoriaDelete.as_view(), name="deletar-categoria"),
    path('excluir/formaPagamento/<int:pk>/', FormaPagamentoDelete.as_view(), name="deletar-formaPagamento"),
    path('excluir/formaEnvio/<int:pk>/', FormaEnvioDelete.as_view(), name="deletar-formaEnvio"),
    path('excluir/venda/<int:pk>/', VendaDelete.as_view(), name="deletar-venda"),
    
    #List View
    path('listar/estados/', EstadoList.as_view(), name="listar-estados"),
    path('listar/cidades/', CidadeList.as_view(), name="listar-cidades"),
    path('listar/pessoas/', PessoaList.as_view(), name="listar-pessoas"),
    path('listar/produtos/', ProdutoList.as_view(), name="listar-produtos"),
    path('listar/categorias/', CategoriaList.as_view(), name="listar-categorias"),
    path('listar/formaPagamentos/', FormaPagamentoList.as_view(), name="listar-formaPagamentos"),
    path('listar/formaEnvios/', FormaEnvioList.as_view(), name="listar-formaEnvios"),
    path('listar/vendas/', VendaList.as_view(), name="listar-vendas"),

    

]
