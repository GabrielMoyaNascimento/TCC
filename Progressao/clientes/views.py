from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from cadastros.models import Categoria, Produto, Pessoa, Venda, ProdutoVenda, Cupom,Parcela
from .models import Carrinho
from django.contrib.auth.models import User,Group



class PaginaInicial(TemplateView):
    template_name = 'clientes/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        # Filtra a categoria
        cat = self.request.GET.get('categoria')  # Recebe a página atual
        # Se existir, filta pelo nome da categoria
        if cat:
            produtos = Produto.objects.filter(
                categoria__nome=cat).reverse()  # [0:9]
        # se não, busca todos
        else:
            # [0:9] # Busca os produtos
            produtos = Produto.objects.all().reverse()

        paginator = Paginator(produtos, 9)  # Divide os produtos em páginas
        page = self.request.GET.get('pagina')  # Recebe a página atual
        produtos = paginator.get_page(page)  # Filtra os produtos dessa página
        context['produtos'] = produtos

        context['categorias'] = Categoria.objects.all()
        return context


class CarrinhoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/carrinho.html'


class PagamentoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/pagamento.html'


class ContatoView( TemplateView):
    template_name = 'clientes/contato.html'


class ConfirmacaoView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/confirmacao.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        venda = Venda.objects.filter(usuario=self.request.user).first()
        context['ultima_venda'] = venda
        context['produtos_venda'] = ProdutoVenda.objects.filter(venda=venda)
        context["parcela"] = Parcela.objects.filter(venda=venda)
        return context


class ConfirmacaoDetalhes(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/confirmacao.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        venda = get_object_or_404(Venda, pk=kwargs['id_venda'], usuario=self.request.user)
        context['ultima_venda'] = venda
        context['produtos_venda'] = ProdutoVenda.objects.filter(venda=venda)
        context["parcela"] = Parcela.objects.filter(venda=venda)
        return context

class Verificar(TemplateView):
    
    def dispatch(self, *args, **kwargs):
        # Verifica se o usuário está logado
        user = self.request.user
        if user.groups.filter(name='Administrador'):
            return redirect('cadastrar-index')    
        elif user.groups.filter(name='Clientes'):
            return redirect('clientes-index')
        else:
            return redirect('login')



# View para adicionar produtos no Carrinho
class AdicionarProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # Também não vai ter template, só colocamos isso porque é obrigatório
    template_name = 'clientes/carrinho.html'

    # Método executado para processar a requisição. É executado antes de renderizar o template
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Recebe a quantidade da url
        qtde = int(kwargs['quantidade'])
        if qtde <= 0:
            return redirect('clientes-carrinho')
            
        # Busca os dados do produto que esta na URL
        prod = get_object_or_404(Produto, pk=kwargs['id_produto'])
       #Se o produto ja estiver no carrinho, ele aumenta a quantidade
        carrinho_tem = False
        carrinho = Carrinho.objects.filter(usuario=self.request.user)
        for c in carrinho:
            if c.produto == prod:
                c.quantidade = c.quantidade + qtde
                if c.quantidade <= prod.estoque:
                    c.save()
                #Informar o usuario caso else
                else:
                    raise Http404("O produto {} não tem a quantidade desejada no estoque.".format(c.produto.nome))
                carrinho_tem = True
                break


        # Cria um objeto "Carrinho" com os dados do produto e a quantidade da URL
        if carrinho_tem == False and qtde <= prod.estoque:

            carrinho = Carrinho.objects.create(
                quantidade=kwargs['quantidade'],
                produto=prod,
                valor_unid=prod.valorVenda,
                usuario=self.request.user)
        else:
            raise Http404("O produto {} não tem a quantidade desejada no estoque.".format(prod.nome))
        # Redireciona o usuário para a lista
        return redirect('clientes-carrinho')


# View para excluir itens do carrinho
class ExcluirProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # defini qual o modelo pra classe, só pra não bugar
    template_name = "clientes/carrinho.html"
    
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Busca o objeto do carrinho que está na URL
        carrinho = get_object_or_404(Carrinho, pk=kwargs['id_carrinho'])
        # Deleta esse carrinho (objeto)
        carrinho.delete()

        # depois de remover, já redirecina o usuário de novo pra lista
        # Ou seja, o excluir nem tela vai ter... ele vai deletar e voltar pra lista
        return redirect('clientes-carrinho')
    

# View para excluir itens do carrinho
class AtualizarProdutoCarrinho(LoginRequiredMixin, TemplateView):
    # defini qual o modelo pra classe, só pra não bugar
    template_name = "clientes/carrinho.html"
    
    def dispatch(self, *args, **kwargs):

        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return redirect('login')

        # Busca o objeto do carrinho que está na URL
        carrinho = get_object_or_404(Carrinho, pk=kwargs['id_carrinho'])
        # Busca a quantidade nova e transforma pra int
        qtde = int(kwargs['quantidade'])
        
        # Se a quantidade for zero, remove ele, se não atualiza
        if(qtde <= 0):
            carrinho.delete()
        else:
            # Verifica se tem em estoque
            if(carrinho.produto.estoque >= qtde):
                # Atualiza o objeto, adicionando a qtde na quantidade
                carrinho.quantidade = qtde
            else:
                carrinho.quantidade = carrinho.produto.estoque

            # Salva o objeto
            carrinho.save()
    

        # depois de remover, já redirecina o usuário de novo pra lista
        # Ou seja, o excluir nem tela vai ter... ele vai deletar e voltar pra lista
        return redirect('clientes-carrinho')
    

# View para listar o carrinho para o usuário
class CarrinhoList(LoginRequiredMixin, ListView):
    model = Carrinho
    template_name = "clientes/carrinho.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        #Pegando valor total dos produtos
        carrinho = Carrinho.objects.filter(usuario=self.request.user)
        total = 0
        for c in carrinho:
            total += c.valor_unid * c.quantidade
        
        # Listar tudo do carrinho desse usuário
        context["carrinho"] = carrinho
        context["valor"] = total

        return context

#View para lista detalhada de apenas um produto
class ProdutoDetailView(DetailView):
    template_name = "clientes/paginaProduto.html"
    model = Produto


#Criando a venda
class VendaCreate(LoginRequiredMixin, CreateView):
    model = Venda
    fields = ['desconto', 'forma_pagamento', 'parcelas', 'forma_envio']
    template_name = 'clientes/pagamento.html'
    success_url = reverse_lazy('clientes-confirmacao')
    login_url = reverse_lazy('login')

    def form_valid(self, form):

        # buscar todos os objetos da classe Carrinho no banco
        produtosCarrinho = Carrinho.objects.filter(usuario=self.request.user)
        pessoa = Pessoa.objects.filter(usuario=self.request.user)

        for p in produtosCarrinho:
            if p.quantidade > p.produto.estoque:
                form.add_error(None, 'Houve um problema ao fazer a venda. O produto {} não tem a quantidade desejada em estoque'.format(p.produto.nome))
                return self.form_invalid(form)

        for pe in pessoa:
            if pe.rg == None or pe.rg == '':
                form.add_error(None, 'O cadastro de usuário não foi finalizado')
                return self.form_invalid(form)
        # if produtosCarrinho == None:
        #     form.errors(None, "Nenhum item no carrinho")
        #     return form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user

        # Valida o desconto, caso tenha
        if form.instance.desconto is None or form.instance.desconto == '':
            form.instance.desconto = ''

        # Executa o form_valid padrão para validar e salvar no banco de dados
        url = super().form_valid(form)

        # Cria uma variável pra essa venda
        valorTotal = 0

        """ Agora temos a venda no banco, vamos pegar os produtos do carrinho e salvar nessa venda """
        # Para cada produto no carrinho, salva no ItemsVenda (foreach)
        for carrinho in produtosCarrinho:

            # Calcula o subtotal = quantidade x valor do produto
            # Atualiza o valor total da venda
            valorTotal += carrinho.produto.valorVenda * carrinho.quantidade

            # Cria um objeto no ProdutoVenda no banco de dados para saber os produtos que foram vendidos
            ProdutoVenda.objects.create(
                preco=carrinho.produto.valorVenda * carrinho.quantidade,
                qtde=carrinho.quantidade,
                produto=carrinho.produto,
                venda=self.object
            )

            # Da baixa no estoque no produto
            carrinho.produto.estoque = carrinho.produto.estoque - carrinho.quantidade

            # Atualiza o produto no banco de dados
            carrinho.produto.save()

            # Deleta o item do carrinho
            carrinho.delete()

        # Verifica se tem cupom e busca ele
        try:
            cupom = Cupom.objects.get(nome=self.object.desconto.upper())
            desconto = valorTotal * cupom.desconto / 100
        except:
            cupom = ''    
            desconto = 0
            self.object.desconto = ''

        # Define o valor bruto (sem desconto)
        self.object.valor = valorTotal
        # Calcula o valor com desconto
        self.object.valor -= desconto
        self.object.valor += self.object.forma_envio.valor
        # Salva a venda
        self.object.save()
            
        i=1
        parcelas = int(self.object.parcelas)
        valorTotal = self.object.valor
        valor_parcela = round((valorTotal / parcelas),2) 
        for i in range (1,parcelas+1):

            if i == parcelas:
                Parcela.objects.create(
                    venda=self.object,
                    numero_parcela = i,
                    valor_parcela = valorTotal 
                )
            else:
                valorTotal -= valor_parcela
                Parcela.objects.create(
                    venda=self.object,
                    numero_parcela = i,
                    valor_parcela = valor_parcela 
                )



                

        # Fim do form_valid
        return url

    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super().get_context_data(*args, **kwargs)

        context["pessoa"] = Pessoa.objects.get(usuario=self.request.user)

        context["produtosCarrinho"] = Carrinho.objects.filter(usuario=self.request.user)
        total = 0
        for c in context["produtosCarrinho"]:
            total += c.produto.valorVenda * c.quantidade

        context["valor"] = total

        # Devolve/envia o context para seu comportamento padrão
        return context
