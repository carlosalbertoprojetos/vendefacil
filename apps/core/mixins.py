"""
Mixin classes for common functionality.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class FormErrorMixin:
    """
    Mixin para tratamento de erros em formulários.
    Fornece métodos comuns para validação e tratamento de erros.
    """

    def add_error_message(self, field_name, message):
        """Adiciona uma mensagem de erro para um campo específico"""
        if field_name not in self.errors:
            self.errors[field_name] = []
        self.errors[field_name].append(message)

    def add_non_field_error(self, message):
        """Adiciona uma mensagem de erro não relacionada a um campo específico"""
        if not hasattr(self, '_non_field_errors'):
            self._non_field_errors = []
        self._non_field_errors.append(message)

    def clean_required_field(self, field_name, field_value, min_length=1, max_length=None):
        """
        Validação comum para campos obrigatórios.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            min_length: Comprimento mínimo (padrão: 1)
            max_length: Comprimento máximo (opcional)
            
        Returns:
            Valor limpo do campo
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip()
        
        if len(field_value) < min_length:
            raise ValidationError(f"O campo {field_name} deve ter pelo menos {min_length} caracteres.")
            
        if max_length and len(field_value) > max_length:
            raise ValidationError(f"O campo {field_name} deve ter no máximo {max_length} caracteres.")
            
        return field_value

    def clean_email_field(self, field_name, field_value):
        """
        Validação comum para campos de email.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            
        Returns:
            Email limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip().lower()
        
        if len(field_value) > 254:
            raise ValidationError(f"O campo {field_name} deve ter no máximo 254 caracteres.")
            
        # Verificar formato do email
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, field_value):
            raise ValidationError(f"Digite um {field_name} válido.")
            
        return field_value

    def clean_phone_field(self, field_name, field_value, required_digits=11):
        """
        Validação comum para campos de telefone.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            required_digits: Número de dígitos esperados (padrão: 11)
            
        Returns:
            Telefone limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip()
        
        # Remove todos os caracteres não numéricos
        phone_digits = "".join(filter(str.isdigit, field_value))
        
        if len(phone_digits) != required_digits:
            if required_digits == 11:
                raise ValidationError(f"O {field_name} deve ter 11 dígitos (ex: 11999999999).")
            elif required_digits == 10:
                raise ValidationError(f"O {field_name} deve ter 10 dígitos (ex: 1133334444).")
            else:
                raise ValidationError(f"O {field_name} deve ter {required_digits} dígitos.")
                
        # Verificar se o DDD é válido (11-99)
        ddd = phone_digits[:2]
        if not (11 <= int(ddd) <= 99):
            raise ValidationError("DDD inválido.")
            
        # Verificar se o número não é sequencial
        if phone_digits == phone_digits[0] * required_digits:
            raise ValidationError(f"Número de {field_name} inválido.")
            
        return field_value

    def clean_cep_field(self, field_name, field_value):
        """
        Validação comum para campos de CEP.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            
        Returns:
            CEP limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip()
        
        # Remove todos os caracteres não numéricos
        cep_digits = "".join(filter(str.isdigit, field_value))
        
        if len(cep_digits) != 8:
            raise ValidationError(f"O {field_name} deve ter 8 dígitos.")
            
        return field_value

    def clean_cpf_field(self, field_name, field_value):
        """
        Validação comum para campos de CPF.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            
        Returns:
            CPF limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip()
        
        # Remove todos os caracteres não numéricos
        cpf_digits = "".join(filter(str.isdigit, field_value))
        
        if len(cpf_digits) != 11:
            raise ValidationError(f"O {field_name} deve ter 11 dígitos.")
            
        # Verificar se não é uma sequência de números iguais
        if cpf_digits == cpf_digits[0] * 11:
            raise ValidationError(f"{field_name} inválido.")
            
        # Validar CPF usando algoritmo
        if not self._validar_cpf(cpf_digits):
            raise ValidationError(f"{field_name} inválido.")
            
        return field_value

    def clean_cnpj_field(self, field_name, field_value):
        """
        Validação comum para campos de CNPJ.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            
        Returns:
            CNPJ limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        field_value = field_value.strip()
        
        # Remove todos os caracteres não numéricos
        cnpj_digits = "".join(filter(str.isdigit, field_value))
        
        if len(cnpj_digits) != 14:
            raise ValidationError(f"O {field_name} deve ter 14 dígitos.")
            
        # Validar CNPJ usando algoritmo
        if not self._validar_cnpj(cnpj_digits):
            raise ValidationError(f"{field_name} inválido.")
            
        return field_value

    def clean_price_field(self, field_name, field_value, min_value=0, max_value=999999.99):
        """
        Validação comum para campos de preço.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            min_value: Valor mínimo (padrão: 0)
            max_value: Valor máximo (padrão: 999999.99)
            
        Returns:
            Preço validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if field_value is None:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        if field_value < min_value:
            raise ValidationError(f"O {field_name} deve ser maior ou igual a {min_value}.")
            
        if field_value > max_value:
            raise ValidationError(f"O {field_name} deve ser menor que {max_value}.")
            
        return field_value

    def clean_quantity_field(self, field_name, field_value, min_value=1, max_value=999):
        """
        Validação comum para campos de quantidade.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            min_value: Valor mínimo (padrão: 1)
            max_value: Valor máximo (padrão: 999)
            
        Returns:
            Quantidade validada
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if field_value is None:
            raise ValidationError(f"O campo {field_name} é obrigatório.")
            
        if field_value < min_value:
            raise ValidationError(f"A {field_name} deve ser pelo menos {min_value}.")
            
        if field_value > max_value:
            raise ValidationError(f"A {field_name} deve ser menor que {max_value}.")
            
        return field_value

    def clean_text_field(self, field_name, field_value, min_length=1, max_length=None, 
                        allow_special_chars=True, required=True):
        """
        Validação comum para campos de texto.
        
        Args:
            field_name: Nome do campo
            field_value: Valor do campo
            min_length: Comprimento mínimo (padrão: 1)
            max_length: Comprimento máximo (opcional)
            allow_special_chars: Permitir caracteres especiais (padrão: True)
            required: Campo obrigatório (padrão: True)
            
        Returns:
            Texto limpo e validado
            
        Raises:
            ValidationError: Se a validação falhar
        """
        if not field_value:
            if required:
                raise ValidationError(f"O campo {field_name} é obrigatório.")
            return field_value
            
        field_value = field_value.strip()
        
        if len(field_value) < min_length:
            raise ValidationError(f"O campo {field_name} deve ter pelo menos {min_length} caracteres.")
            
        if max_length and len(field_value) > max_length:
            raise ValidationError(f"O campo {field_name} deve ter no máximo {max_length} caracteres.")
            
        if not allow_special_chars:
            import re
            if not re.match(r'^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$', field_value):
                raise ValidationError(f"O campo {field_name} deve conter apenas letras e espaços.")
                
        return field_value

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

    def _validar_cnpj(self, cnpj):
        """Valida CNPJ usando algoritmo"""
        if len(cnpj) != 14:
            return False
            
        # Verificar se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
            
        # Calcular primeiro dígito verificador
        soma = 0
        peso = 2
        for i in range(12, 0, -1):
            soma += int(cnpj[i-1]) * peso
            peso += 1
            if peso > 9:
                peso = 2
        resto = soma % 11
        if resto < 2:
            dv1 = 0
        else:
            dv1 = 11 - resto
            
        # Calcular segundo dígito verificador
        soma = 0
        peso = 2
        for i in range(13, 0, -1):
            soma += int(cnpj[i-1]) * peso
            peso += 1
            if peso > 9:
                peso = 2
        resto = soma % 11
        if resto < 2:
            dv2 = 0
        else:
            dv2 = 11 - resto
            
        return int(cnpj[12]) == dv1 and int(cnpj[13]) == dv2


class ViewErrorMixin:
    """
    Mixin para tratamento de erros em views.
    Fornece métodos comuns para exibição de mensagens de erro.
    """

    def add_error_message(self, request, message, level=messages.ERROR):
        """Adiciona uma mensagem de erro"""
        messages.add_message(request, level, message)

    def add_success_message(self, request, message):
        """Adiciona uma mensagem de sucesso"""
        messages.add_message(request, messages.SUCCESS, message)

    def add_warning_message(self, request, message):
        """Adiciona uma mensagem de aviso"""
        messages.add_message(request, messages.WARNING, message)

    def add_info_message(self, request, message):
        """Adiciona uma mensagem informativa"""
        messages.add_message(request, messages.INFO, message)

    def handle_form_errors(self, request, form):
        """Trata erros de formulário e exibe mensagens apropriadas"""
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        self.add_error_message(request, error)
                    else:
                        self.add_error_message(request, f"{field}: {error}")

    def handle_validation_error(self, request, error):
        """Trata erros de validação"""
        if isinstance(error, ValidationError):
            if hasattr(error, 'message'):
                self.add_error_message(request, error.message)
            elif hasattr(error, 'messages'):
                for message in error.messages:
                    self.add_error_message(request, message)
            else:
                self.add_error_message(request, str(error))
        else:
            self.add_error_message(request, str(error))
