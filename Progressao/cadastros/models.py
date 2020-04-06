from django.db import models
from django.contrib.auth.models import User


class Estado(models.Model):
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.sigla + " - " + self.nome


class Cidade(models.Model):
    nome = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + " - " + self.estado.sigla


class Pessoa(models.Model):

    nome = models.CharField(max_length=50, verbose_name="Qual seu nome?", help_text="Digite seu nome completo", null=True)
    nascimento = models.DateField(verbose_name='data de nascimento', null=True)
    endereco = models.CharField(max_length=100, null=True)
    numero = models.CharField(max_length=10, verbose_name="Número", null=True)
    cep = models.CharField(max_length=25, null=True)
    rg = models.CharField(max_length=25, null=True)
    cpf = models.CharField(max_length=25, null=True)
    telefone = models.CharField(max_length=25, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, null=True)
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        if self.nome:
            return f"{self.nome} - Usuário: {self.usuario}"
        else:
            return f"Dados incompletos - Usuário: {self.usuario}"
        




class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
   

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class FormaEnvio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    data_da_venda = models.DateTimeField(auto_now=True)
    desconto = models.DecimalField(max_digits=50, decimal_places=2)
    valor = models.DecimalField(max_digits=50, decimal_places=2)
    parcelas = models.IntegerField()
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    forma_envio = models.ForeignKey(FormaEnvio, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.usuario + " - " + self.usuario.nome,
        self.forma_pagamento + " - " + self.forma_pagamento.nome,
        self.forma_envio + " - " + self.forma_envio.nome


class Produto(models.Model):
    codigo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    estoque = models.IntegerField()
    valorVenda = models.DecimalField(max_digits=50, decimal_places=2)
    imagem = models.ImageField(upload_to="imagens/%Y/%m/%d/", max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.categoria.nome + " - " + self.categoria.nome


class ProdutoVenda(models.Model):
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    qtde = models.IntegerField()
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)

    def __str__(self):
        return "[Venda ID: " + str(self.venda.pk) + "] " + self.produto.nome + " x " + str(self.qtde) + " = " + str(self.preco)
