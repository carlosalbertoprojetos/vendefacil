"""
Custom validators for VendaSimples project.
"""

import re
from django.core.exceptions import ValidationError


def validate_cpf(value):
    """Valida CPF"""
    if not value:
        return

    # Remove caracteres não numéricos
    cpf = re.sub(r"[^0-9]", "", value)

    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cpf[9]) != digito1:
        raise ValidationError("CPF inválido.")

    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cpf[10]) != digito2:
        raise ValidationError("CPF inválido.")


def validate_cnpj(value):
    """Valida CNPJ"""
    if not value:
        return

    # Remove caracteres não numéricos
    cnpj = re.sub(r"[^0-9]", "", value)

    if len(cnpj) != 14:
        raise ValidationError("CNPJ deve ter 14 dígitos.")

    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        raise ValidationError("CNPJ inválido.")

    # Validação do primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cnpj[12]) != digito1:
        raise ValidationError("CNPJ inválido.")

    # Validação do segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cnpj[13]) != digito2:
        raise ValidationError("CNPJ inválido.")


def validate_phone(value):
    """Valida telefone brasileiro"""
    if not value:
        return

    # Remove caracteres não numéricos
    phone = re.sub(r"[^0-9]", "", value)

    # Telefone deve ter 10 ou 11 dígitos
    if len(phone) not in [10, 11]:
        raise ValidationError("Telefone deve ter 10 ou 11 dígitos.")

    # Primeiro dígito deve ser diferente de 0
    if phone[0] == "0":
        raise ValidationError("Telefone inválido.")

    # Validação removida: celular não precisa mais começar com 9 no segundo dígito


def validate_cep(value):
    """Valida CEP brasileiro"""
    if not value:
        return

    # Remove caracteres não numéricos
    cep = re.sub(r"[^0-9]", "", value)

    if len(cep) != 8:
        raise ValidationError("CEP deve ter 8 dígitos.")

    # CEP não pode ser todos zeros ou todos iguais
    if cep == "0" * 8 or cep == cep[0] * 8:
        raise ValidationError("CEP inválido.")
