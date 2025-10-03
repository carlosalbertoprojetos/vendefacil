"""
Forms for pagamento app.
"""

from django import forms
from django.core.exceptions import ValidationError


class CheckoutForm(forms.Form):
    """Formulário para checkout"""

    # Dados do cliente
    cliente_nome = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nome Completo"
    )
    cliente_telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "(00) 00000-0000"
        }),
        label="Telefone"
    )
    cliente_email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="E-mail"
    )
    cliente_cpf = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "000.000.000-00"
        }),
        label="CPF"
    )

    # Endereço de entrega
    endereco_cep = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "00000-000"
        }),
        label="CEP"
    )
    endereco_logradouro = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Logradouro"
    )
    endereco_numero = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Número"
    )
    endereco_complemento = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Complemento"
    )
    endereco_bairro = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Bairro"
    )
    endereco_cidade = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Cidade"
    )
    endereco_estado = forms.CharField(
        max_length=2,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": "2"
        }),
        label="Estado"
    )

    # Método de pagamento
    metodo_pagamento = forms.ChoiceField(
        choices=[
            ("pix", "PIX"),
            ("cartao_credito", "Cartão de Crédito"),
            ("cartao_debito", "Cartão de Débito"),
            ("boleto", "Boleto Bancário"),
            ("dinheiro", "Dinheiro"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Método de Pagamento"
    )

    # Dados do cartão (se aplicável)
    cartao_numero = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "0000 0000 0000 0000",
            "placeholder": "0000 0000 0000 0000"
        }),
        label="Número do Cartão"
    )
    cartao_nome = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nome no Cartão"
    )
    cartao_validade = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "00/00",
            "placeholder": "MM/AA"
        }),
        label="Validade"
    )
    cartao_cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "data-mask": "000",
            "placeholder": "000"
        }),
        label="CVV"
    )

    # Observações
    observacoes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Observações sobre o pedido"
        }),
        label="Observações"
    )

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
        
        if not cliente_email:
            raise ValidationError("O email do cliente é obrigatório.")
            
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

    def clean_metodo_pagamento(self):
        """Validação do método de pagamento"""
        metodo_pagamento = self.cleaned_data.get("metodo_pagamento")
        
        if not metodo_pagamento:
            raise ValidationError("O método de pagamento é obrigatório.")
            
        return metodo_pagamento

    def clean_cartao_numero(self):
        """Validação do número do cartão"""
        cartao_numero = self.cleaned_data.get("cartao_numero")
        metodo_pagamento = self.cleaned_data.get("metodo_pagamento")
        
        if metodo_pagamento in ["cartao_credito", "cartao_debito"]:
            if not cartao_numero:
                raise ValidationError("O número do cartão é obrigatório.")
                
            cartao_numero = cartao_numero.strip()
            
            # Remove todos os caracteres não numéricos
            cartao_digits = "".join(filter(str.isdigit, cartao_numero))
            
            if len(cartao_digits) < 13 or len(cartao_digits) > 19:
                raise ValidationError("Número do cartão inválido.")
                
            # Validar usando algoritmo de Luhn
            if not self._validar_cartao(cartao_digits):
                raise ValidationError("Número do cartão inválido.")
                
        return cartao_numero

    def clean_cartao_nome(self):
        """Validação do nome no cartão"""
        cartao_nome = self.cleaned_data.get("cartao_nome")
        metodo_pagamento = self.cleaned_data.get("metodo_pagamento")
        
        if metodo_pagamento in ["cartao_credito", "cartao_debito"]:
            if not cartao_nome:
                raise ValidationError("O nome no cartão é obrigatório.")
                
            cartao_nome = cartao_nome.strip()
            
            if len(cartao_nome) < 2:
                raise ValidationError("O nome no cartão deve ter pelo menos 2 caracteres.")
                
            if len(cartao_nome) > 255:
                raise ValidationError("O nome no cartão deve ter no máximo 255 caracteres.")
                
            # Verificar caracteres válidos
            import re
            if not re.match(r'^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$', cartao_nome):
                raise ValidationError("O nome no cartão deve conter apenas letras e espaços.")
                
        return cartao_nome

    def clean_cartao_validade(self):
        """Validação da validade do cartão"""
        cartao_validade = self.cleaned_data.get("cartao_validade")
        metodo_pagamento = self.cleaned_data.get("metodo_pagamento")
        
        if metodo_pagamento in ["cartao_credito", "cartao_debito"]:
            if not cartao_validade:
                raise ValidationError("A validade do cartão é obrigatória.")
                
            cartao_validade = cartao_validade.strip()
            
            if len(cartao_validade) != 5 or cartao_validade[2] != "/":
                raise ValidationError("A validade deve estar no formato MM/AA.")
                
            try:
                mes = int(cartao_validade[:2])
                ano = int(cartao_validade[3:])
                
                if mes < 1 or mes > 12:
                    raise ValidationError("Mês inválido.")
                    
                # Verificar se não está vencido
                from datetime import datetime
                ano_atual = datetime.now().year % 100
                mes_atual = datetime.now().month
                
                if ano < ano_atual or (ano == ano_atual and mes < mes_atual):
                    raise ValidationError("Cartão vencido.")
                    
            except ValueError:
                raise ValidationError("Data inválida.")
                
        return cartao_validade

    def clean_cartao_cvv(self):
        """Validação do CVV do cartão"""
        cartao_cvv = self.cleaned_data.get("cartao_cvv")
        metodo_pagamento = self.cleaned_data.get("metodo_pagamento")
        
        if metodo_pagamento in ["cartao_credito", "cartao_debito"]:
            if not cartao_cvv:
                raise ValidationError("O CVV do cartão é obrigatório.")
                
            cartao_cvv = cartao_cvv.strip()
            
            if len(cartao_cvv) < 3 or len(cartao_cvv) > 4:
                raise ValidationError("CVV inválido.")
                
            if not cartao_cvv.isdigit():
                raise ValidationError("O CVV deve conter apenas números.")
                
        return cartao_cvv

    def clean_observacoes(self):
        """Validação das observações"""
        observacoes = self.cleaned_data.get("observacoes")
        
        if observacoes:
            observacoes = observacoes.strip()
            
            if len(observacoes) > 1000:
                raise ValidationError("As observações devem ter no máximo 1000 caracteres.")
                
        return observacoes

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        metodo_pagamento = cleaned_data.get("metodo_pagamento")
        
        # Verificar se os campos do cartão são obrigatórios quando o método é cartão
        if metodo_pagamento in ["cartao_credito", "cartao_debito"]:
            cartao_numero = cleaned_data.get("cartao_numero")
            cartao_nome = cleaned_data.get("cartao_nome")
            cartao_validade = cleaned_data.get("cartao_validade")
            cartao_cvv = cleaned_data.get("cartao_cvv")
            
            if not all([cartao_numero, cartao_nome, cartao_validade, cartao_cvv]):
                raise ValidationError("Todos os dados do cartão são obrigatórios.")
                
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

    def _validar_cartao(self, numero):
        """Valida número do cartão usando algoritmo de Luhn"""
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10

        return luhn_checksum(numero) == 0
