from django.urls import path
from .views import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Importa as views que a gente criou 
from .views import PaginaInicial,SobreView, AjudaView

# Tem que ser urlpatterns porque é padrão do Django
urlpatterns = [
    # Todo path tem endereço, sua_view.as_view() e nome
    path('', PaginaInicial.as_view(), name='index'),
    path('paginas/sobre.html/',SobreView.as_view(), name='sobre'),
    path('paginas/ajuda.html/', AjudaView.as_view(), name='ajuda'),
    
]
