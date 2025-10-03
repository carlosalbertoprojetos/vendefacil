"""
Product models for VendaSimples project.
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel, SoftDeleteModel, AuditModel
from apps.core.managers import ActiveManager, SoftDeleteManager, ActiveSoftDeleteManager


class Categoria(TimeStampedModel, SoftDeleteModel):
    """Categoria principal de produtos"""

    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    imagem = models.ImageField(
        upload_to="categorias/", null=True, blank=True, verbose_name="Imagem"
    )
    ordem = models.IntegerField(default=0, verbose_name="Ordem")

    objects = models.Manager()
    active_objects = ActiveSoftDeleteManager()

    class Meta:
        db_table = "categorias"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["ordem", "nome"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "ordem"]),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    @property
    def total_produtos(self):
        """Retorna total de produtos ativos nesta categoria"""
        return (
            self.subcategorias.filter(is_active=True).aggregate(
                total=models.Count(
                    "produtos", filter=models.Q(produtos__is_active=True)
                )
            )["total"]
            or 0
        )


class Subcategoria(TimeStampedModel, SoftDeleteModel):
    """Subcategoria de produtos"""

    nome = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    imagem = models.ImageField(
        upload_to="subcategorias/", null=True, blank=True, verbose_name="Imagem"
    )
    ordem = models.IntegerField(default=0, verbose_name="Ordem")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="subcategorias",
        verbose_name="Categoria",
    )

    objects = models.Manager()
    active_objects = ActiveSoftDeleteManager()

    class Meta:
        db_table = "subcategorias"
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"
        ordering = ["categoria__ordem", "categoria__nome", "ordem", "nome"]
        unique_together = ["categoria", "slug"]
        indexes = [
            models.Index(fields=["categoria", "slug"]),
            models.Index(fields=["is_active", "ordem"]),
        ]

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    @property
    def total_produtos(self):
        """Retorna total de produtos ativos nesta subcategoria"""
        return self.produtos.filter(is_active=True).count()


class Produto(TimeStampedModel, SoftDeleteModel):
    """Modelo de produto"""

    # Informações Básicas
    nome = models.CharField(max_length=255, db_index=True, verbose_name="Nome")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    descricao = models.TextField(verbose_name="Descrição")
    descricao_curta = models.CharField(
        max_length=255, blank=True, verbose_name="Descrição Curta"
    )

    # Preço e Estoque
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True,
        validators=[MinValueValidator(0)],
        verbose_name="Preço",
    )
    preco_promocional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Preço Promocional",
    )
    estoque = models.IntegerField(
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
        verbose_name="Estoque",
    )

    # Identificação
    codigo = models.CharField(
        max_length=50, unique=True, db_index=True, verbose_name="Código", blank=True
    )
    sku = models.CharField(max_length=50, blank=True, verbose_name="SKU")
    ean = models.CharField(max_length=13, blank=True, verbose_name="EAN")
    marca = models.CharField(max_length=100, blank=True, verbose_name="Marca")

    # Relacionamentos
    vendedor = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="produtos",
        verbose_name="Vendedor",
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name="produtos",
        verbose_name="Categoria",
    )
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produtos",
        verbose_name="Subcategoria",
    )

    # Status
    disponivel = models.BooleanField(
        default=True, db_index=True, verbose_name="Disponível"
    )
    em_destaque = models.BooleanField(
        default=False, db_index=True, verbose_name="Em Destaque"
    )
    em_promocao = models.BooleanField(
        default=False, db_index=True, verbose_name="Em Promoção"
    )
    mais_vendido = models.BooleanField(
        default=False, db_index=True, verbose_name="Mais Vendido"
    )
    lancamento = models.BooleanField(
        default=False, db_index=True, verbose_name="Lançamento"
    )

    # Estatísticas
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
    vendas = models.IntegerField(default=0, verbose_name="Vendas")

    objects = models.Manager()
    active_objects = ActiveSoftDeleteManager()

    class Meta:
        db_table = "produtos"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["vendedor", "is_active"]),
            models.Index(fields=["categoria", "is_active"]),
            models.Index(fields=["subcategoria", "is_active"]),
            models.Index(fields=["preco"]),
            models.Index(fields=["estoque"]),
            models.Index(fields=["codigo"]),
            models.Index(fields=["em_destaque", "is_active"]),
            models.Index(fields=["disponivel", "is_active"]),
            models.Index(fields=["em_promocao", "is_active"]),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)

    def gerar_codigo(self):
        """Gera código único para o produto"""
        import random
        import string

        while True:
            codigo = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            if not Produto.objects.filter(codigo=codigo).exists():
                return codigo

    @property
    def preco_final(self):
        """Retorna preço promocional se disponível, senão preço normal"""
        if self.em_promocao and self.preco_promocional:
            return self.preco_promocional
        return self.preco

    @property
    def tem_estoque(self):
        """Verifica se tem estoque"""
        return self.estoque > 0

    @property
    def estoque_baixo(self):
        """Verifica se estoque está baixo"""
        return self.estoque <= self.estoque_minimo

    @property
    def imagem_principal(self):
        """Retorna primeira imagem ou None"""
        return self.imagens.filter(is_principal=True).first() or self.imagens.first()

    def incrementar_visualizacao(self):
        """Incrementa contador de visualizações"""
        self.visualizacoes += 1
        self.save(update_fields=["visualizacoes"])


class ImagemProduto(TimeStampedModel):
    """Imagens do produto"""

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="imagens",
        verbose_name="Produto",
    )
    imagem = models.ImageField(upload_to="produtos/imagens/", verbose_name="Imagem")
    thumbnail = models.ImageField(
        upload_to="produtos/thumbnails/",
        null=True,
        blank=True,
        verbose_name="Thumbnail",
    )
    is_principal = models.BooleanField(default=False, verbose_name="Imagem Principal")
    ordem = models.IntegerField(default=0, verbose_name="Ordem")
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto Alternativo"
    )

    class Meta:
        db_table = "imagens_produto"
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ["ordem", "created_at"]

    def __str__(self):
        return f"Imagem de {self.produto.nome}"

    def save(self, *args, **kwargs):
        # Se marcada como principal, desmarca outras
        if self.is_principal:
            ImagemProduto.objects.filter(
                produto=self.produto, is_principal=True
            ).exclude(pk=self.pk).update(is_principal=False)
        super().save(*args, **kwargs)


class ProdutoVariacao(TimeStampedModel):
    """Variações do produto (tamanho, cor, etc.)"""

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="variacoes",
        verbose_name="Produto",
    )
    nome = models.CharField(max_length=100, verbose_name="Nome da Variação")
    valor = models.CharField(max_length=100, verbose_name="Valor")
    preco_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Preço Adicional",
    )
    estoque = models.IntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name="Estoque"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        db_table = "produto_variacoes"
        verbose_name = "Variação do Produto"
        verbose_name_plural = "Variações dos Produtos"
        unique_together = ["produto", "nome", "valor"]

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}: {self.valor}"


class ProdutoAtributo(TimeStampedModel):
    """Atributos do produto (material, cor, etc.)"""

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="atributos",
        verbose_name="Produto",
    )
    nome = models.CharField(max_length=100, verbose_name="Nome do Atributo")
    valor = models.CharField(max_length=255, verbose_name="Valor")

    class Meta:
        db_table = "produto_atributos"
        verbose_name = "Atributo do Produto"
        verbose_name_plural = "Atributos dos Produtos"
        unique_together = ["produto", "nome"]

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}: {self.valor}"
