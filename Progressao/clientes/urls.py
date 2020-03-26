from django.urls import path
# Importa as views que a gente criou 
from .views import *
# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    
    path('clientes/index/', PaginaInicial.as_view(), name="clientes-index"),
    path('clientes/carrinho/', Carrinho.as_view(), name="clientes-carrinho"),
    path('clientes/login/', Login.as_view(), name="clientes-login"),
    path('clientes/novaConta/', Cadastro.as_view(), name="clientes-novaConta"),
]
