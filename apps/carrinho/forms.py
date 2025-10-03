"""
Forms for carrinho app.
"""

from django import forms
from django.core.exceptions import ValidationError
from apps.produtos.models import Produto


class AddToCartForm(forms.Form):
    """Formulário para adicionar produto ao carrinho"""

    produto_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    quantidade = forms.IntegerField(
        min_value=1,
        max_value=999,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "1",
            "max": "999",
            "value": "1"
        }),
        label="Quantidade"
    )
    variacao = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: Tamanho M, Cor Azul"
        }),
        label="Variação"
    )

    def clean_produto_id(self):
        """Validação do ID do produto"""
        produto_id = self.cleaned_data.get("produto_id")
        
        if not produto_id:
            raise ValidationError("ID do produto é obrigatório.")
            
        try:
            produto = Produto.objects.get(id=produto_id, is_active=True)
        except Produto.DoesNotExist:
            raise ValidationError("Produto não encontrado.")
            
        if not produto.disponivel:
            raise ValidationError("Este produto não está disponível.")
            
        return produto_id

    def clean_quantidade(self):
        """Validação da quantidade"""
        quantidade = self.cleaned_data.get("quantidade")
        
        if not quantidade:
            raise ValidationError("A quantidade é obrigatória.")
            
        if quantidade < 1:
            raise ValidationError("A quantidade deve ser pelo menos 1.")
            
        if quantidade > 999:
            raise ValidationError("A quantidade deve ser menor que 999.")
            
        return quantidade

    def clean_variacao(self):
        """Validação da variação"""
        variacao = self.cleaned_data.get("variacao")
        
        if variacao:
            variacao = variacao.strip()
            
            if len(variacao) > 255:
                raise ValidationError("A variação deve ter no máximo 255 caracteres.")
                
        return variacao

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        produto_id = cleaned_data.get("produto_id")
        quantidade = cleaned_data.get("quantidade")
        
        if produto_id and quantidade:
            try:
                produto = Produto.objects.get(id=produto_id, is_active=True)
                
                # Verificar se há estoque suficiente
                if produto.estoque < quantidade:
                    raise ValidationError(
                        f"Estoque insuficiente. Disponível: {produto.estoque} unidades."
                    )
                    
            except Produto.DoesNotExist:
                raise ValidationError("Produto não encontrado.")
                
        return cleaned_data


class UpdateCartItemForm(forms.Form):
    """Formulário para atualizar item do carrinho"""

    item_id = forms.CharField(
        widget=forms.HiddenInput()
    )
    quantidade = forms.IntegerField(
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "0",
            "max": "999"
        }),
        label="Quantidade"
    )

    def clean_item_id(self):
        """Validação do ID do item"""
        item_id = self.cleaned_data.get("item_id")
        
        if not item_id:
            raise ValidationError("ID do item é obrigatório.")
            
        return item_id

    def clean_quantidade(self):
        """Validação da quantidade"""
        quantidade = self.cleaned_data.get("quantidade")
        
        if quantidade is None:
            raise ValidationError("A quantidade é obrigatória.")
            
        if quantidade < 0:
            raise ValidationError("A quantidade não pode ser negativa.")
            
        if quantidade > 999:
            raise ValidationError("A quantidade deve ser menor que 999.")
            
        return quantidade


class RemoveFromCartForm(forms.Form):
    """Formulário para remover item do carrinho"""

    item_id = forms.CharField(
        widget=forms.HiddenInput()
    )

    def clean_item_id(self):
        """Validação do ID do item"""
        item_id = self.cleaned_data.get("item_id")
        
        if not item_id:
            raise ValidationError("ID do item é obrigatório.")
            
        return item_id


class ClearCartForm(forms.Form):
    """Formulário para limpar carrinho"""

    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Confirmo que desejo limpar o carrinho"
    )

    def clean_confirm(self):
        """Validação da confirmação"""
        confirm = self.cleaned_data.get("confirm")
        
        if not confirm:
            raise ValidationError("Você deve confirmar para limpar o carrinho.")
            
        return confirm


class ApplyCouponForm(forms.Form):
    """Formulário para aplicar cupom de desconto"""

    codigo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o código do cupom"
        }),
        label="Código do Cupom"
    )

    def clean_codigo(self):
        """Validação do código do cupom"""
        codigo = self.cleaned_data.get("codigo")
        
        if not codigo:
            raise ValidationError("O código do cupom é obrigatório.")
            
        codigo = codigo.strip().upper()
        
        if len(codigo) < 3:
            raise ValidationError("O código do cupom deve ter pelo menos 3 caracteres.")
            
        if len(codigo) > 50:
            raise ValidationError("O código do cupom deve ter no máximo 50 caracteres.")
            
        # Verificar caracteres válidos
        import re
        if not re.match(r'^[A-Z0-9\-_]+$', codigo):
            raise ValidationError("O código do cupom deve conter apenas letras maiúsculas, números, hífens e underscores.")
            
        return codigo


class CalculateShippingForm(forms.Form):
    """Formulário para calcular frete"""

    cep = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "00000-000",
            "placeholder": "00000-000"
        }),
        label="CEP"
    )

    def clean_cep(self):
        """Validação do CEP"""
        cep = self.cleaned_data.get("cep")
        
        if not cep:
            raise ValidationError("O CEP é obrigatório.")
            
        cep = cep.strip()
        
        # Remove todos os caracteres não numéricos
        cep_digits = "".join(filter(str.isdigit, cep))
        
        if len(cep_digits) != 8:
            raise ValidationError("O CEP deve ter 8 dígitos.")
            
        return cep
