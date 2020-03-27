from django.db import models
from django.contrib.auth.models import User

from cadastros.models import Produto




class Carrinho(models.Model):
    quantidade = models.IntegerField()
    valor_unid = models.DecimalField(max_digits=50, decimal_places=2)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.produto + " x" + self.valor_unid + "x" + self.produto.imagem
