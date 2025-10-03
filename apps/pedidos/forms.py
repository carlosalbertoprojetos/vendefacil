"""
Forms for pedidos app.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Pedido, ItemPedido, StatusPedido
from apps.produtos.models import Produto


class PedidoForm(forms.ModelForm):
    """Formulário para pedido"""

    class Meta:
        model = Pedido
        fields = [
            "cliente_nome",
            "cliente_telefone",
            "cliente_email",
            "cliente_cpf",
            "endereco_cep",
            "endereco_logradouro",
            "endereco_numero",
            "endereco_complemento",
            "endereco_bairro",
            "endereco_cidade",
            "endereco_estado",
            "subtotal",
            "desconto",
            "frete",
            "observacoes",
            "data_entrega_prevista",
        ]
        widgets = {
            "cliente_nome": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_telefone": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 00000-0000"}
            ),
            "cliente_email": forms.EmailInput(attrs={"class": "form-control"}),
            "cliente_cpf": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "000.000.000-00"}
            ),
            "endereco_cep": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "00000-000"}
            ),
            "endereco_logradouro": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_numero": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_complemento": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_bairro": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_cidade": forms.TextInput(attrs={"class": "form-control"}),
            "endereco_estado": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "2"}
            ),
            "subtotal": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "readonly": True}
            ),
            "desconto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "frete": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "observacoes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "data_entrega_prevista": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }

    def clean_cliente_nome(self):
        """Validação do nome do cliente"""
        cliente_nome = self.cleaned_data.get("cliente_nome")
        
        if not cliente_nome:
            raise ValidationError("O nome do cliente é obrigatório.")
            
        cliente_nome = cliente_nome.strip()
        
        if len(cliente_nome) < 2:
            raise ValidationError("O nome do cliente deve ter pelo menos 2 caracteres.")
            
        if len(cliente_nome) > 255:
            raise ValidationError("O nome do cliente deve ter no máximo 255 caracteres.")
            
        # Verificar caracteres válidos
        import re
        if not re.match(r'^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$', cliente_nome):
            raise ValidationError("O nome do cliente deve conter apenas letras e espaços.")
            
        return cliente_nome

    def clean_cliente_telefone(self):
        """Validação do telefone do cliente"""
        cliente_telefone = self.cleaned_data.get("cliente_telefone")
        
        if not cliente_telefone:
            raise ValidationError("O telefone do cliente é obrigatório.")
            
        cliente_telefone = cliente_telefone.strip()
        
        # Remove todos os caracteres não numéricos
        telefone_digits = "".join(filter(str.isdigit, cliente_telefone))
        
        if len(telefone_digits) != 11:
            raise ValidationError("O telefone deve ter 11 dígitos (ex: 11999999999).")
            
        # Verificar se o DDD é válido (11-99)
        ddd = telefone_digits[:2]
        if not (11 <= int(ddd) <= 99):
            raise ValidationError("DDD inválido.")
            
        # Verificar se o número não é sequencial
        if telefone_digits == telefone_digits[0] * 11:
            raise ValidationError("Número de telefone inválido.")
            
        return cliente_telefone

    def clean_cliente_email(self):
        """Validação do email do cliente"""
        cliente_email = self.cleaned_data.get("cliente_email")
        
        if cliente_email:
            cliente_email = cliente_email.strip().lower()
            
            if len(cliente_email) > 254:
                raise ValidationError("O email deve ter no máximo 254 caracteres.")
                
            # Verificar formato do email
            import re
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, cliente_email):
                raise ValidationError("Digite um email válido.")
                
        return cliente_email

    def clean_cliente_cpf(self):
        """Validação do CPF do cliente"""
        cliente_cpf = self.cleaned_data.get("cliente_cpf")
        
        if cliente_cpf:
            cliente_cpf = cliente_cpf.strip()
            
            # Remove todos os caracteres não numéricos
            cpf_digits = "".join(filter(str.isdigit, cliente_cpf))
            
            if len(cpf_digits) != 11:
                raise ValidationError("O CPF deve ter 11 dígitos.")
                
            # Verificar se não é uma sequência de números iguais
            if cpf_digits == cpf_digits[0] * 11:
                raise ValidationError("CPF inválido.")
                
            # Validar CPF usando algoritmo
            if not self._validar_cpf(cpf_digits):
                raise ValidationError("CPF inválido.")
                
        return cliente_cpf

    def clean_endereco_cep(self):
        """Validação do CEP"""
        endereco_cep = self.cleaned_data.get("endereco_cep")
        
        if not endereco_cep:
            raise ValidationError("O CEP é obrigatório.")
            
        endereco_cep = endereco_cep.strip()
        
        # Remove todos os caracteres não numéricos
        cep_digits = "".join(filter(str.isdigit, endereco_cep))
        
        if len(cep_digits) != 8:
            raise ValidationError("O CEP deve ter 8 dígitos.")
            
        return endereco_cep

    def clean_endereco_logradouro(self):
        """Validação do logradouro"""
        endereco_logradouro = self.cleaned_data.get("endereco_logradouro")
        
        if not endereco_logradouro:
            raise ValidationError("O logradouro é obrigatório.")
            
        endereco_logradouro = endereco_logradouro.strip()
        
        if len(endereco_logradouro) < 3:
            raise ValidationError("O logradouro deve ter pelo menos 3 caracteres.")
            
        if len(endereco_logradouro) > 255:
            raise ValidationError("O logradouro deve ter no máximo 255 caracteres.")
            
        return endereco_logradouro

    def clean_endereco_numero(self):
        """Validação do número"""
        endereco_numero = self.cleaned_data.get("endereco_numero")
        
        if not endereco_numero:
            raise ValidationError("O número é obrigatório.")
            
        endereco_numero = endereco_numero.strip()
        
        if len(endereco_numero) < 1:
            raise ValidationError("O número é obrigatório.")
            
        if len(endereco_numero) > 20:
            raise ValidationError("O número deve ter no máximo 20 caracteres.")
            
        return endereco_numero

    def clean_endereco_bairro(self):
        """Validação do bairro"""
        endereco_bairro = self.cleaned_data.get("endereco_bairro")
        
        if not endereco_bairro:
            raise ValidationError("O bairro é obrigatório.")
            
        endereco_bairro = endereco_bairro.strip()
        
        if len(endereco_bairro) < 2:
            raise ValidationError("O bairro deve ter pelo menos 2 caracteres.")
            
        if len(endereco_bairro) > 100:
            raise ValidationError("O bairro deve ter no máximo 100 caracteres.")
            
        return endereco_bairro

    def clean_endereco_cidade(self):
        """Validação da cidade"""
        endereco_cidade = self.cleaned_data.get("endereco_cidade")
        
        if not endereco_cidade:
            raise ValidationError("A cidade é obrigatória.")
            
        endereco_cidade = endereco_cidade.strip()
        
        if len(endereco_cidade) < 2:
            raise ValidationError("A cidade deve ter pelo menos 2 caracteres.")
            
        if len(endereco_cidade) > 100:
            raise ValidationError("A cidade deve ter no máximo 100 caracteres.")
            
        return endereco_cidade

    def clean_endereco_estado(self):
        """Validação do estado"""
        endereco_estado = self.cleaned_data.get("endereco_estado")
        
        if not endereco_estado:
            raise ValidationError("O estado é obrigatório.")
            
        endereco_estado = endereco_estado.strip().upper()
        
        if len(endereco_estado) != 2:
            raise ValidationError("O estado deve ter 2 caracteres (ex: SP).")
            
        # Lista de estados válidos
        estados_validos = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        
        if endereco_estado not in estados_validos:
            raise ValidationError("Estado inválido.")
            
        return endereco_estado

    def clean_subtotal(self):
        """Validação do subtotal"""
        subtotal = self.cleaned_data.get("subtotal")
        
        if subtotal is None:
            raise ValidationError("O subtotal é obrigatório.")
            
        if subtotal < 0:
            raise ValidationError("O subtotal não pode ser negativo.")
            
        if subtotal > 999999.99:
            raise ValidationError("O subtotal deve ser menor que R$ 999.999,99.")
            
        return subtotal

    def clean_desconto(self):
        """Validação do desconto"""
        desconto = self.cleaned_data.get("desconto")
        
        if desconto is None:
            desconto = 0
            
        if desconto < 0:
            raise ValidationError("O desconto não pode ser negativo.")
            
        if desconto > 999999.99:
            raise ValidationError("O desconto deve ser menor que R$ 999.999,99.")
            
        return desconto

    def clean_frete(self):
        """Validação do frete"""
        frete = self.cleaned_data.get("frete")
        
        if frete is None:
            frete = 0
            
        if frete < 0:
            raise ValidationError("O frete não pode ser negativo.")
            
        if frete > 999999.99:
            raise ValidationError("O frete deve ser menor que R$ 999.999,99.")
            
        return frete

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        subtotal = cleaned_data.get("subtotal")
        desconto = cleaned_data.get("desconto")
        frete = cleaned_data.get("frete")
        
        if subtotal and desconto and subtotal < desconto:
            raise ValidationError("O desconto não pode ser maior que o subtotal.")
            
        return cleaned_data

    def _validar_cpf(self, cpf):
        """Valida CPF usando algoritmo"""
        if len(cpf) != 11:
            return False
            
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
            
        # Calcular primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        if resto < 2:
            dv1 = 0
        else:
            dv1 = 11 - resto
            
        # Calcular segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        if resto < 2:
            dv2 = 0
        else:
            dv2 = 11 - resto
            
        return int(cpf[9]) == dv1 and int(cpf[10]) == dv2


class ItemPedidoForm(forms.ModelForm):
    """Formulário para item do pedido"""

    class Meta:
        model = ItemPedido
        fields = [
            "produto",
            "quantidade",
            "preco_unitario",
            "variacao",
        ]
        widgets = {
            "produto": forms.Select(attrs={"class": "form-control"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control"}),
            "preco_unitario": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "variacao": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas produtos ativos
        self.fields["produto"].queryset = Produto.objects.filter(
            disponivel=True, is_active=True
        ).order_by("nome")

    def clean_produto(self):
        """Validação do produto"""
        produto = self.cleaned_data.get("produto")
        
        if not produto:
            raise ValidationError("O produto é obrigatório.")
            
        if not produto.disponivel:
            raise ValidationError("Este produto não está disponível.")
            
        return produto

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

    def clean_preco_unitario(self):
        """Validação do preço unitário"""
        preco_unitario = self.cleaned_data.get("preco_unitario")
        
        if not preco_unitario:
            raise ValidationError("O preço unitário é obrigatório.")
            
        if preco_unitario <= 0:
            raise ValidationError("O preço unitário deve ser maior que zero.")
            
        if preco_unitario > 999999.99:
            raise ValidationError("O preço unitário deve ser menor que R$ 999.999,99.")
            
        return preco_unitario

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
        produto = cleaned_data.get("produto")
        quantidade = cleaned_data.get("quantidade")
        
        if produto and quantidade:
            # Verificar se há estoque suficiente
            if produto.estoque < quantidade:
                raise ValidationError(
                    f"Estoque insuficiente. Disponível: {produto.estoque} unidades."
                )
                
        return cleaned_data


class StatusUpdateForm(forms.Form):
    """Formulário para atualização de status do pedido"""

    status = forms.ChoiceField(
        choices=StatusPedido.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Novo Status"
    )
    observacoes = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3, "placeholder": "Observações sobre a mudança de status"}
        ),
        required=False,
        label="Observações"
    )

    def clean_status(self):
        """Validação do status"""
        status = self.cleaned_data.get("status")
        
        if not status:
            raise ValidationError("O status é obrigatório.")
            
        return status

    def clean_observacoes(self):
        """Validação das observações"""
        observacoes = self.cleaned_data.get("observacoes")
        
        if observacoes:
            observacoes = observacoes.strip()
            
            if len(observacoes) > 1000:
                raise ValidationError("As observações devem ter no máximo 1000 caracteres.")
                
        return observacoes
