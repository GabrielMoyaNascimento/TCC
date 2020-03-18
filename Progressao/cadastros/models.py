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

    nome = models.CharField(max_length=50, verbose_name="Qual seu nome?", help_text="Digite seu nome completo")
    nascimento = models.DateField(verbose_name='data de nascimento')
    email = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=25)
    rg = models.CharField(max_length=25)
    cpf = models.CharField(max_length=25)
    telefone = models.CharField(max_length=25)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + ' - ' + str(self.nascimento),
        

    def form_valid(self, form):

        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user

        url = super().form_valid(form)

        # código a fazer depois de salvar objeto no banco
        self.object.atributo = 'algo'

        # Salva o objeto novamente
        self.object.save()

        return url

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Pessoa.objects.filter(usuario=self.request.user)
        return self.object_list




class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
   

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)


class FormaEnvio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)


class Venda(models.Model):
    data_da_venda = models.DateField(verbose_name='data de nascimento')
    desconto = models.DecimalField(max_digits=50, decimal_places=2)
    valor = models.DecimalField(max_digits=50, decimal_places=2)
    parcelas = models.IntegerField()
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    forma_envio = models.ForeignKey(FormaEnvio, on_delete=models.PROTECT)
    def __str__(self):
        return self.pessoa + " - " + self.pessoa.nome,
        self.forma_pagamento + " - " + self.forma_pagamento.nome,
        self.forma_envio + " - " + self.forma_envio.nome


class Produto(models.Model):
    codigo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    estoque = models.IntegerField()
    valorVenda = models.DecimalField(max_digits=50, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.categoria + " - " + self.categoria.nome


class ProdutoVenda(models.Model):
    quantidade = models.IntegerField()
    valor_envio = models.DecimalField(max_digits=50, decimal_places=2)
    valor_total = models.DecimalField(max_digits=50, decimal_places=2)
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)
    produto = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.produto + " - " + self.produto.valor,
        self.venda + " - " + self.venda.forma_pagamento
