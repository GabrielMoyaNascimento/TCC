from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html',extra_context={'titulo': 'Autenticação'}), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name="logout"),

]
