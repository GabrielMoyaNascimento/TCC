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
    PARCELA_CHOICES = (
          ("1x","À Vista"),
          ("2","2x"),
          ("3","3x"),
        
    )


    data_da_venda = models.DateTimeField(auto_now=True)
    desconto = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=50, decimal_places=2,null=True, blank=True)
    parcelas = models.CharField(max_length = 100, choices = PARCELA_CHOICES)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT,null=True, blank=True)
    forma_envio = models.ForeignKey(FormaEnvio, on_delete=models.PROTECT,null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "[{}] {}".format(self.pk, self.usuario.pessoa.nome)


class Parcela(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)
    numero_parcela = models.DecimalField(max_digits=50, decimal_places=2)
    valor_parcela = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return self.numero_parcela + "-" + self.valor_parcela

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

class EntradaProduto(models.Model):
    quantidade = models.DecimalField(max_digits=8, decimal_places=0)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    data_entrada = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quantidade + " - " + self.produto


class ProdutoVenda(models.Model):
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    qtde = models.IntegerField()
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)

    def __str__(self):
        return "[Venda ID: " + str(self.venda.pk) + "] " + self.produto.nome + " x " + str(self.qtde) + " = " + str(self.preco)


class Cupom(models.Model):
    nome = models.CharField(max_length=100)
    desconto = models.DecimalField(max_digits=3, decimal_places=0)
    validade = models.DateField(verbose_name='data de validade', null=True)

    def __str__(self):
        return self.nome
