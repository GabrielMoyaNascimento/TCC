from django.urls import path
# Importa as views que a gente criou 
from .views import *
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    path('', PaginaInicial.as_view(), name="clientes-index"),
    path('contato/', ContatoView.as_view(), name="clientes-contato"),
    path('confirmacaoCompra/', ConfirmacaoView.as_view(), name="clientes-confirmacao"),
    path('detalhesCompra/<int:id_venda>', ConfirmacaoDetalhes.as_view(), name="detalhe-compra"),
    path('produto/<int:pk>', ProdutoDetailView.as_view(), name="clientes-paginaProduto"),
    
    #Verificar Usuário para redirecionar para a pagina referente a seu grupo
    path('verificar/', Verificar.as_view(), name="verificar"),
    
    path('pagamento/', VendaCreate.as_view(), name="clientes-pagamento"),
    path('adicionar/produto/<int:id_produto>/<int:quantidade>/', AdicionarProdutoCarrinho.as_view(), name="adicionar-produto"),
    path('atualizar/carrinho/<int:id_carrinho>/<int:quantidade>/', AtualizarProdutoCarrinho.as_view(), name="atualizar-carrinho"),
    path('remover/produto/<int:id_carrinho>', ExcluirProdutoCarrinho.as_view(), name="deletar-produto"),
    path('carrinho/', CarrinhoList.as_view(), name="clientes-carrinho"),
]
