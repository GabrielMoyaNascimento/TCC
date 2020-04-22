"""Progressao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# adicionar o include para importar urls dos apps
from django.urls import path, include

# Pra importar o static e o settings
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Importa todas as urls criadas no app páginas
    path('', include('cadastros.urls')),
    path('', include('usuarios.urls')),
    path('', include('erros.urls')),
    path('', include('clientes.urls')),
] 
   
# Configurar as views que estão gerando os erros
handler400 = 'erros.views.handler400'
handler403 = 'erros.views.handler403'
handler404 = 'erros.views.handler404'
handler500 = 'erros.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
