from django.urls import path
# Importa as views que a gente criou 
from .views import *
from usuarios.views import UsuarioCreate
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    path('', PaginaInicial.as_view(), name="clientes-index"),
    path('clientes/contato/', ContatoView.as_view(), name="clientes-contato"),
    path('clientes/confirmacaoCompra/', ConfirmacaoView.as_view(), name="clientes-confirmacao"),
    path('clientes/novaConta/', UsuarioCreate.as_view(), name="clientes-novaConta"),
    path('produto/<int:pk>', ProdutoDetailView.as_view(), name="clientes-paginaProduto"),
    
    # path('clientes/login/', Login.as_view(), name="clientes-login"),
    
    path('adicionar/produto/<int:id_produto>/<int:quantidade>/', AdicionarProdutoCarrinho.as_view(), name="adicionar-produto"),
    path('atualizar/carrinho/<int:id_carrinho>/<int:quantidade>/', AtualizarProdutoCarrinho.as_view(), name="atualizar-carrinho"),
    path('remover/produto/<int:id_carrinho>', ExcluirProdutoCarrinho.as_view(), name="deletar-produto"),
    path('carrinho/', CarrinhoList.as_view(), name="clientes-carrinho"),
]
