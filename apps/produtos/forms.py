"""
Forms for produtos app.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Produto, Categoria, Subcategoria


class ProdutoForm(forms.ModelForm):
    """Formulário para produto"""

    # Campo personalizado para imagem principal
    imagem_principal = forms.ImageField(
        required=False,
        label="Imagem Principal",
        help_text="Selecione uma imagem principal para o produto",
    )

    class Meta:
        model = Produto
        fields = [
            "nome",
            "descricao",
            "descricao_curta",
            "categoria",
            "subcategoria",
            "preco",
            "preco_promocional",
            "estoque",
            "sku",
            "marca",
            "disponivel",
            "em_destaque",
            "em_promocao",
            "mais_vendido",
            "lancamento",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "descricao_curta": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_categoria",
                    "onchange": "loadSubcategorias()",
                }
            ),
            "subcategoria": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_subcategoria",
                    "disabled": True,
                }
            ),
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "preco_promocional": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "estoque": forms.NumberInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "disponivel": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "em_destaque": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "em_promocao": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "mais_vendido": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "lancamento": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classe CSS ao campo de imagem
        self.fields["imagem_principal"].widget.attrs.update({"class": "form-control"})

        # Configurar subcategorias baseadas na categoria selecionada
        if "categoria" in self.data:
            try:
                categoria_id = int(self.data.get("categoria"))
                self.fields["subcategoria"].queryset = Subcategoria.objects.filter(
                    categoria_id=categoria_id, is_active=True
                ).order_by("nome")
                self.fields["subcategoria"].widget.attrs["disabled"] = False
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Se estiver editando um produto existente
            if self.instance.categoria:
                self.fields["subcategoria"].queryset = Subcategoria.objects.filter(
                    categoria=self.instance.categoria, is_active=True
                ).order_by("nome")
                self.fields["subcategoria"].widget.attrs["disabled"] = False
            else:
                self.fields["subcategoria"].queryset = Subcategoria.objects.none()
        else:
            # Se for um novo produto, subcategorias vazias
            self.fields["subcategoria"].queryset = Subcategoria.objects.none()

        # Se estiver editando um produto existente, mostrar a imagem atual
        if self.instance and self.instance.pk:
            try:
                from .models import ImagemProduto

                imagem_principal = ImagemProduto.objects.filter(
                    produto=self.instance, is_principal=True
                ).first()
                if imagem_principal:
                    self.fields["imagem_principal"].help_text = (
                        f"Imagem atual: {imagem_principal.imagem.name}"
                    )
            except:
                pass

    def save(self, commit=True):
        """Salva o produto e cria a imagem principal se fornecida"""
        produto = super().save(commit=commit)

        # Se uma imagem foi fornecida, criar ImagemProduto
        if commit and self.cleaned_data.get("imagem_principal"):
            from .models import ImagemProduto

            # Verificar se já existe uma imagem principal
            imagem_existente = ImagemProduto.objects.filter(
                produto=produto, is_principal=True
            ).first()

            if imagem_existente:
                # Atualizar imagem existente
                imagem_existente.imagem = self.cleaned_data["imagem_principal"]
                imagem_existente.save()
            else:
                # Criar nova imagem principal
                ImagemProduto.objects.create(
                    produto=produto,
                    imagem=self.cleaned_data["imagem_principal"],
                    is_principal=True,
                    ordem=0,
                )

        return produto

    def clean_nome(self):
        """Validação do nome do produto"""
        nome = self.cleaned_data.get("nome")

        if not nome:
            raise ValidationError("O nome do produto é obrigatório.")

        nome = nome.strip()

        if len(nome) < 3:
            raise ValidationError("O nome deve ter pelo menos 3 caracteres.")

        if len(nome) > 255:
            raise ValidationError("O nome deve ter no máximo 255 caracteres.")

        # Verificar caracteres especiais não permitidos
        import re

        if not re.match(
            r"^[a-zA-Z0-9\s\-_.,áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+$", nome
        ):
            raise ValidationError(
                "O nome contém caracteres inválidos. Use apenas letras, números, espaços e os seguintes caracteres: - _ . ,"
            )

        # Verificar se já existe produto com mesmo nome (exceto o próprio)
        queryset = Produto.objects.filter(nome__iexact=nome)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError("Já existe um produto com este nome.")

        return nome

    def clean_preco(self):
        """Validação do preço"""
        preco = self.cleaned_data.get("preco")

        if preco is None:
            raise ValidationError("O preço é obrigatório.")

        if preco <= 0:
            raise ValidationError("O preço deve ser maior que zero.")

        if preco > 999999.99:
            raise ValidationError("O preço deve ser menor que R$ 999.999,99.")

        return preco

    def clean_preco_promocional(self):
        """Validação do preço promocional"""
        preco_promocional = self.cleaned_data.get("preco_promocional")
        preco = self.cleaned_data.get("preco")

        if preco_promocional is not None:
            if preco_promocional <= 0:
                raise ValidationError("O preço promocional deve ser maior que zero.")

            if preco_promocional > 999999.99:
                raise ValidationError(
                    "O preço promocional deve ser menor que R$ 999.999,99."
                )

            if preco and preco_promocional >= preco:
                raise ValidationError(
                    "O preço promocional deve ser menor que o preço normal."
                )

        return preco_promocional

    def clean_estoque(self):
        """Validação do estoque"""
        estoque = self.cleaned_data.get("estoque")

        if estoque is None:
            raise ValidationError("O estoque é obrigatório.")

        if estoque < 0:
            raise ValidationError("O estoque não pode ser negativo.")

        if estoque > 999999:
            raise ValidationError("O estoque deve ser menor que 999.999 unidades.")

        return estoque

    def clean_sku(self):
        """Validação do SKU"""
        sku = self.cleaned_data.get("sku")

        if sku:
            sku = sku.strip()

            if len(sku) < 3:
                raise ValidationError("O SKU deve ter pelo menos 3 caracteres.")

            if len(sku) > 50:
                raise ValidationError("O SKU deve ter no máximo 50 caracteres.")

            # Verificar caracteres válidos para SKU
            import re

            if not re.match(r"^[A-Z0-9\-_]+$", sku.upper()):
                raise ValidationError(
                    "O SKU deve conter apenas letras maiúsculas, números, hífens e underscores."
                )

            # Verificar se já existe produto com mesmo SKU (exceto o próprio)
            queryset = Produto.objects.filter(sku__iexact=sku)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise ValidationError("Já existe um produto com este SKU.")

            return sku.upper()

        return sku

    def clean_descricao(self):
        """Validação da descrição"""
        descricao = self.cleaned_data.get("descricao")

        if descricao:
            descricao = descricao.strip()

            if len(descricao) < 10:
                raise ValidationError("A descrição deve ter pelo menos 10 caracteres.")

            if len(descricao) > 2000:
                raise ValidationError("A descrição deve ter no máximo 2000 caracteres.")

        return descricao

    def clean_descricao_curta(self):
        """Validação da descrição curta"""
        descricao_curta = self.cleaned_data.get("descricao_curta")

        if descricao_curta:
            descricao_curta = descricao_curta.strip()

            if len(descricao_curta) < 5:
                raise ValidationError(
                    "A descrição curta deve ter pelo menos 5 caracteres."
                )

            if len(descricao_curta) > 200:
                raise ValidationError(
                    "A descrição curta deve ter no máximo 200 caracteres."
                )

        return descricao_curta

    def clean_marca(self):
        """Validação da marca"""
        marca = self.cleaned_data.get("marca")

        if marca:
            marca = marca.strip()

            if len(marca) < 2:
                raise ValidationError("A marca deve ter pelo menos 2 caracteres.")

            if len(marca) > 100:
                raise ValidationError("A marca deve ter no máximo 100 caracteres.")

            # Verificar caracteres válidos para marca
            import re

            if not re.match(
                r"^[a-zA-Z0-9\s\-_.,áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+$", marca
            ):
                raise ValidationError("A marca contém caracteres inválidos.")

        return marca

    def clean_subcategoria(self):
        """Validação da subcategoria"""
        subcategoria = self.cleaned_data.get("subcategoria")
        categoria = self.cleaned_data.get("categoria")

        if subcategoria and categoria:
            if subcategoria.categoria != categoria:
                raise ValidationError(
                    "A subcategoria deve pertencer à categoria selecionada."
                )

        return subcategoria


class CategoriaForm(forms.ModelForm):
    """Formulário para categoria"""

    class Meta:
        model = Categoria
        fields = [
            "nome",
            "descricao",
            "imagem",
            "ordem",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "imagem": forms.FileInput(attrs={"class": "form-control"}),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_nome(self):
        """Validação do nome da categoria"""
        nome = self.cleaned_data.get("nome")

        if not nome:
            raise ValidationError("O nome da categoria é obrigatório.")

        nome = nome.strip()

        if len(nome) < 2:
            raise ValidationError("O nome deve ter pelo menos 2 caracteres.")

        if len(nome) > 100:
            raise ValidationError("O nome deve ter no máximo 100 caracteres.")

        # Verificar caracteres especiais não permitidos
        import re

        if not re.match(
            r"^[a-zA-Z0-9\s\-_.,áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+$", nome
        ):
            raise ValidationError(
                "O nome contém caracteres inválidos. Use apenas letras, números, espaços e os seguintes caracteres: - _ . ,"
            )

        # Verificar se já existe categoria com mesmo nome (exceto a própria)
        queryset = Categoria.objects.filter(nome__iexact=nome)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError("Já existe uma categoria com este nome.")

        return nome

    def clean_ordem(self):
        """Validação da ordem"""
        ordem = self.cleaned_data.get("ordem")

        if ordem is not None:
            if ordem < 0:
                raise ValidationError("A ordem não pode ser negativa.")

            if ordem > 9999:
                raise ValidationError("A ordem deve ser menor que 9999.")

        return ordem


class SubcategoriaForm(forms.ModelForm):
    """Formulário para subcategoria"""

    class Meta:
        model = Subcategoria
        fields = [
            "nome",
            "descricao",
            "imagem",
            "ordem",
            "categoria",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "imagem": forms.FileInput(attrs={"class": "form-control"}),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_nome(self):
        """Validação do nome da subcategoria"""
        nome = self.cleaned_data.get("nome")

        if not nome:
            raise ValidationError("O nome da subcategoria é obrigatório.")

        nome = nome.strip()

        if len(nome) < 2:
            raise ValidationError("O nome deve ter pelo menos 2 caracteres.")

        if len(nome) > 100:
            raise ValidationError("O nome deve ter no máximo 100 caracteres.")

        # Verificar caracteres especiais não permitidos
        import re

        if not re.match(
            r"^[a-zA-Z0-9\s\-_.,áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+$", nome
        ):
            raise ValidationError(
                "O nome contém caracteres inválidos. Use apenas letras, números, espaços e os seguintes caracteres: - _ . ,"
            )

        return nome

    def clean_ordem(self):
        """Validação da ordem"""
        ordem = self.cleaned_data.get("ordem")

        if ordem is not None:
            if ordem < 0:
                raise ValidationError("A ordem não pode ser negativa.")

            if ordem > 9999:
                raise ValidationError("A ordem deve ser menor que 9999.")

        return ordem

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        categoria = cleaned_data.get("categoria")

        if nome and categoria:
            # Verificar se já existe subcategoria com mesmo nome na mesma categoria
            queryset = Subcategoria.objects.filter(
                nome__iexact=nome.strip(), categoria=categoria
            )
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise ValidationError(
                    f'Já existe uma subcategoria com o nome "{nome}" na categoria "{categoria.nome}".'
                )

        return cleaned_data
