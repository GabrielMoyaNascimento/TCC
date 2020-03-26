from django.db import models
# from cadastros.models import *
from django.contrib.auth.models import User

from cadastros.models import Produto

# class Pessoa(models.Model):

#     nome = models.CharField(
#         max_length=50, verbose_name="Qual seu nome?", help_text="Digite seu nome completo")
#     nascimento = models.DateField(verbose_name='data de nascimento')
#     email = models.CharField(max_length=100)
#     endereco = models.CharField(max_length=100)
#     numero = models.CharField(max_length=10)
#     cep = models.CharField(max_length=25)
#     rg = models.CharField(max_length=25)
#     cpf = models.CharField(max_length=25)
#     telefone = models.CharField(max_length=25)
#     # cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
#     usuario = models.OneToOneField(User, on_delete=models.PROTECT)

#     def __str__(self):
#         return self.nome + ' - ' + str(self.email)


class Carrinho(models.Model):
    quantidade = models.IntegerField()
    valor_unid = models.DecimalField(max_digits=50, decimal_places=2)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.produto + " x" + self.valor_unid
