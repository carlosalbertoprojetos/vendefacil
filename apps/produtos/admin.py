"""
Admin configuration for produtos app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria,
    Subcategoria,
    Produto,
    ImagemProduto,
    ProdutoVariacao,
    ProdutoAtributo,
)


class ImagemProdutoInline(admin.TabularInline):
    """Inline para imagens do produto"""

    model = ImagemProduto
    extra = 1
    fields = ("imagem", "is_principal", "ordem", "alt_text")


class ProdutoVariacaoInline(admin.TabularInline):
    """Inline para variações do produto"""

    model = ProdutoVariacao
    extra = 1
    fields = ("nome", "valor", "preco_adicional", "estoque", "ativo")


class ProdutoAtributoInline(admin.TabularInline):
    """Inline para atributos do produto"""

    model = ProdutoAtributo
    extra = 1
    fields = ("nome", "valor")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para Categoria"""

    list_display = ("nome", "ordem", "total_produtos", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("nome", "descricao")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("ordem", "nome")

    fieldsets = (
        ("Informações Básicas", {"fields": ("nome", "slug", "descricao", "ordem")}),
        ("Imagem", {"fields": ("imagem",)}),
        ("Status", {"fields": ("is_active", "deleted_at")}),
    )


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    """Admin para Subcategoria"""

    list_display = (
        "nome",
        "categoria",
        "ordem",
        "total_produtos",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "categoria", "created_at")
    search_fields = ("nome", "descricao", "categoria__nome")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("categoria__ordem", "categoria__nome", "ordem", "nome")

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("nome", "slug", "descricao", "categoria", "ordem")},
        ),
        ("Imagem", {"fields": ("imagem",)}),
        ("Status", {"fields": ("is_active", "deleted_at")}),
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """Admin para Produto"""

    list_display = (
        "nome",
        "vendedor",
        "categoria",
        "subcategoria",
        "preco",
        "estoque",
        "disponivel",
        "em_destaque",
        "visualizacoes",
        "created_at",
    )
    list_filter = (
        "disponivel",
        "em_destaque",
        "em_promocao",
        "mais_vendido",
        "lancamento",
        "categoria",
        "subcategoria",
        "vendedor",
        "created_at",
    )
    search_fields = ("nome", "codigo", "sku", "marca")
    prepopulated_fields = {"slug": ("nome",)}
    readonly_fields = ("codigo", "visualizacoes", "vendas", "created_at", "updated_at")

    inlines = [ImagemProdutoInline, ProdutoVariacaoInline, ProdutoAtributoInline]

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("nome", "slug", "descricao", "descricao_curta", "codigo")},
        ),
        (
            "Preço e Estoque",
            {"fields": ("preco", "preco_promocional", "estoque")},
        ),
        ("Identificação", {"fields": ("sku", "ean", "marca")}),
        ("Relacionamentos", {"fields": ("vendedor", "categoria", "subcategoria")}),
        (
            "Status",
            {
                "fields": (
                    "disponivel",
                    "em_destaque",
                    "em_promocao",
                    "mais_vendido",
                    "lancamento",
                )
            },
        ),
        (
            "Estatísticas",
            {"fields": ("visualizacoes", "vendas"), "classes": ("collapse",)},
        ),
        (
            "Status do Sistema",
            {"fields": ("is_active", "deleted_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        """Otimiza queries"""
        return (
            super()
            .get_queryset(request)
            .select_related("vendedor", "categoria", "subcategoria")
            .prefetch_related("imagens")
        )


@admin.register(ImagemProduto)
class ImagemProdutoAdmin(admin.ModelAdmin):
    """Admin para ImagemProduto"""

    list_display = ("produto", "is_principal", "ordem", "imagem_preview", "created_at")
    list_filter = ("is_principal", "created_at")
    search_fields = ("produto__nome", "alt_text")
    ordering = ("produto", "ordem")

    def imagem_preview(self, obj):
        """Preview da imagem"""
        if obj.imagem:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.imagem.url,
            )
        return "-"

    imagem_preview.short_description = "Preview"


@admin.register(ProdutoVariacao)
class ProdutoVariacaoAdmin(admin.ModelAdmin):
    """Admin para ProdutoVariacao"""

    list_display = ("produto", "nome", "valor", "preco_adicional", "estoque", "ativo")
    list_filter = ("nome", "ativo", "created_at")
    search_fields = ("produto__nome", "nome", "valor")


@admin.register(ProdutoAtributo)
class ProdutoAtributoAdmin(admin.ModelAdmin):
    """Admin para ProdutoAtributo"""

    list_display = ("produto", "nome", "valor")
    list_filter = ("nome", "created_at")
    search_fields = ("produto__nome", "nome", "valor")
