from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.email)



class Categoria(models.Model): # Categorias (Masculino, Feminino, Infantil)
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.nome)


class Tipo(models.Model): # Tipos (Camisa, Camiseta, Bermuda, Calça)
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.nome)


class Produto(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.ForeignKey(Tipo, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Nome: {self.nome}, Categoria: {self.categoria}, Tipo: {self.tipo}, Preço: {self.preco}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagem:
            img = Image.open(self.imagem.path)
            tamanho_fixo = (400, 600)
            img = img.resize(tamanho_fixo)
            img.save(self.imagem.path)
    
    def total_vendas(self):
        itens = ItensPedido.objects.filter(pedido__finalizado=True, item_estoque__produto=self.id)
        total = sum([item.quantidade for item in itens])
        return total
    

class Cor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.nome)

class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)  # produto (ex: camisa)
    cor = models.ForeignKey(Cor, null=True, blank=True, on_delete=models.SET_NULL) # cor (ex: azul, laranja, verde)
    tamanho = models.CharField(max_length=200, null=True, blank=True) # tamanho (ex: P, M, G)
    quantidade = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.produto.nome}, Tamanho: {self.tamanho}, Cor: {self.cor}, Quantidade: {self.quantidade}"


class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.cliente} - {self.rua} - {self.cidade} - {self.estado} - {self.cep}"


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"Cliente: {self.cliente.email} - id_pedido: {self.id} - Finalizado: {self.finalizado}"
    
    @property
    def quantidade_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        quantidade = sum([item.quantidade for item in itens_pedido])
        return quantidade

    @property
    def preco_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        preco = sum([item.preco_total for item in itens_pedido])
        return preco
        
    @property
    def itens(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        return itens_pedido
    

class ItensPedido(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"Id pedido: {self.pedido.id} - Produto {self.item_estoque.produto.nome}, {self.item_estoque.tamanho}, {self.item_estoque.cor.nome}"

    @property
    def preco_total(self):
        return self.quantidade * self.item_estoque.produto.preco

class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.link_destino} - ativo: {self.ativo}"


class Pagamento(models.Model):
    id_pagamento = models.CharField(max_length=400)
    pedido = models.ForeignKey(Pedido, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    aprovado = models.BooleanField(default=False)