from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import UsuarioCreate, PessoaUpdate, PerfilView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html',extra_context={'titulo': 'Autenticação'}), name = 'login'),
    path('sair/', auth_views.LogoutView.as_view(), name="logout"),
    path('registrar/', UsuarioCreate.as_view(), name="clientes-novaConta"),
    path('perfil/', PerfilView.as_view(), name="clientes-perfil"),
    path('alterar/perfil/', PessoaUpdate.as_view(), name="clientes-alterar-perfil"),
    
    #Alterar senha View
    path('alterar-minha-senha/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/login.html',
        extra_context={'titulo': 'Alterar senha atual'}, 
        success_url=reverse_lazy('index')
    ), name="alterar-senha"),
    
    path('esqueci-senha/',
         auth_views.PasswordResetView.as_view(template_name='senha/password_reset_form.html'), name='password_reset'),

    path('senha-enviada/',
         auth_views.PasswordResetDoneView.as_view(template_name='senha/password_reset_done.html'), name='password_reset_done'),

    path('redefinir-senha/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='senha/password_reset_confirm.html'), name='password_reset_confirm'),

    path('senha-atualizada/',
         auth_views.PasswordResetCompleteView.as_view(template_name='senha/password_reset_complete.html'), name='password_reset_complete'),




]
