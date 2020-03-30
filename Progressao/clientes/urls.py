from django.urls import path
# Importa as views que a gente criou 
from .views import *
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    path('clientes/index/', PaginaInicial.as_view(), name="clientes-index"),
    path('clientes/contato/', ContatoView.as_view(), name="clientes-contato"),
    path('clientes/confirmacaoCompra/', ConfirmacaoView.as_view(), name="clientes-confirmacao"),
    path('clientes/login/', Login.as_view(), name="clientes-login"),
    path('clientes/novaConta/', Cadastro.as_view(), name="clientes-novaConta"),
    path('clientes/paginaProduto/<int:pk>', ProdutoDetailView.as_view(), name="clientes-paginaProduto"),
    path('clientes/novaConta/cadastrar', CadastroCreate.as_view(), name="clientes-cadastrar"),
    
    path('adicionar/produto/<int:id_produto>/<int:quantidade>/', AdicionarProdutoCarrinho.as_view(), name="adicionar-produto"),
    path('atualizar/carrinho/<int:id_carrinho>/<int:quantidade>/', AtualizarProdutoCarrinho.as_view(), name="atualizar-carrinho"),
    path('remover/produto/<int:id_carrinho>', ExcluirProdutoCarrinho.as_view(), name="deletar-produto"),
    path('carrinho/', CarrinhoList.as_view(), name="clientes-carrinho"),
]
