"""
Forms for authentication app.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Empresa, Profile
from apps.core.validators import validate_cpf, validate_cnpj


class UserRegistrationForm(UserCreationForm):
    """Formulário de registro de usuário"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "seu@email.com"}
        ),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome"}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Sobrenome"}
        ),
    )
    role = forms.ChoiceField(
        choices=[
            ("EMPRESA", "Empresa"),
            ("VENDEDOR", "Vendedor"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "(11) 99999-9999",
                "data-mask": "(00) 00000-0000",
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme sua senha",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError("O email é obrigatório.")

        email = email.strip().lower()

        if len(email) > 254:
            raise ValidationError("O email deve ter no máximo 254 caracteres.")

        # Verificar formato do email
        import re

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValidationError("Digite um email válido.")

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este email já está em uso.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            phone = phone.strip()

            # Remove todos os caracteres não numéricos
            phone_digits = "".join(filter(str.isdigit, phone))

            if len(phone_digits) != 11:
                raise ValidationError(
                    "O telefone deve ter 11 dígitos (ex: 11999999999)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = phone_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

            # Verificar se o número não é sequencial
            if phone_digits == phone_digits[0] * 11:
                raise ValidationError("Número de telefone inválido.")

        return phone

    def clean_first_name(self):
        """Validação do primeiro nome"""
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise ValidationError("O primeiro nome é obrigatório.")

        first_name = first_name.strip()

        if len(first_name) < 2:
            raise ValidationError("O primeiro nome deve ter pelo menos 2 caracteres.")

        if len(first_name) > 150:
            raise ValidationError("O primeiro nome deve ter no máximo 150 caracteres.")

        # Verificar caracteres válidos
        import re

        if not re.match(
            r"^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$", first_name
        ):
            raise ValidationError(
                "O primeiro nome deve conter apenas letras e espaços."
            )

        return first_name

    def clean_last_name(self):
        """Validação do sobrenome"""
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise ValidationError("O sobrenome é obrigatório.")

        last_name = last_name.strip()

        if len(last_name) < 2:
            raise ValidationError("O sobrenome deve ter pelo menos 2 caracteres.")

        if len(last_name) > 150:
            raise ValidationError("O sobrenome deve ter no máximo 150 caracteres.")

        # Verificar caracteres válidos
        import re

        if not re.match(
            r"^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$", last_name
        ):
            raise ValidationError("O sobrenome deve conter apenas letras e espaços.")

        return last_name

    def clean_password1(self):
        """Validação da senha"""
        password1 = self.cleaned_data.get("password1")

        if not password1:
            raise ValidationError("A senha é obrigatória.")

        if len(password1) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")

        if len(password1) > 128:
            raise ValidationError("A senha deve ter no máximo 128 caracteres.")

        # Verificar se a senha não é muito simples
        import re

        if not re.search(r"[A-Z]", password1):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")

        if not re.search(r"[a-z]", password1):
            raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")

        if not re.search(r"[0-9]", password1):
            raise ValidationError("A senha deve conter pelo menos um número.")

        return password1

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("As senhas não coincidem.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = self.cleaned_data["role"]
        user.phone = self.cleaned_data["phone"]

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Formulário de login"""

    email = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email ou nome de usuário",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Senha"}
        )
    )
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def __init__(self, *args, **kwargs):
        # Remove 'request' dos kwargs se estiver presente
        kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Validação do email/username"""
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError("O email é obrigatório.")

        email = email.strip()

        if len(email) > 255:
            raise ValidationError("O email deve ter no máximo 255 caracteres.")

        return email

    def clean_password(self):
        """Validação da senha"""
        password = self.cleaned_data.get("password")

        if not password:
            raise ValidationError("A senha é obrigatória.")

        if len(password) < 1:
            raise ValidationError("A senha não pode estar vazia.")

        return password

    def get_user(self):
        """Retorna o usuário autenticado"""
        from .models import User

        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        return User.objects.authenticate_user(username, password)


class EmpresaForm(forms.ModelForm):
    """Formulário para empresa"""

    class Meta:
        model = Empresa
        fields = [
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "telefone",
            "whatsapp",
            "email",
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "logo",
            "banner",
            "tema_cor_primaria",
            "tema_cor_secundaria",
        ]
        widgets = {
            "razao_social": forms.TextInput(attrs={"class": "form-control"}),
            "nome_fantasia": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "00.000.000/0000-00"}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 0000-0000"}
            ),
            "whatsapp": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 00000-0000"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cep": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "00000-000"}
            ),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "2"}
            ),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "banner": forms.FileInput(attrs={"class": "form-control"}),
            "tema_cor_primaria": forms.TextInput(
                attrs={"class": "form-control", "type": "color"}
            ),
            "tema_cor_secundaria": forms.TextInput(
                attrs={"class": "form-control", "type": "color"}
            ),
        }

    def clean_razao_social(self):
        """Validação da razão social"""
        razao_social = self.cleaned_data.get("razao_social")

        if not razao_social:
            raise ValidationError("A razão social é obrigatória.")

        razao_social = razao_social.strip()

        if len(razao_social) < 3:
            raise ValidationError("A razão social deve ter pelo menos 3 caracteres.")

        if len(razao_social) > 255:
            raise ValidationError("A razão social deve ter no máximo 255 caracteres.")

        return razao_social

    def clean_nome_fantasia(self):
        """Validação do nome fantasia"""
        nome_fantasia = self.cleaned_data.get("nome_fantasia")

        if nome_fantasia:
            nome_fantasia = nome_fantasia.strip()

            if len(nome_fantasia) < 3:
                raise ValidationError(
                    "O nome fantasia deve ter pelo menos 3 caracteres."
                )

            if len(nome_fantasia) > 255:
                raise ValidationError(
                    "O nome fantasia deve ter no máximo 255 caracteres."
                )

        return nome_fantasia

    def clean_cnpj(self):
        """Validação do CNPJ"""
        cnpj = self.cleaned_data.get("cnpj")

        if not cnpj:
            raise ValidationError("O CNPJ é obrigatório.")

        cnpj = cnpj.strip()

        if len(cnpj) < 14:
            raise ValidationError("O CNPJ deve ter 14 dígitos.")

        try:
            validate_cnpj(cnpj)
        except ValidationError as e:
            raise ValidationError(f"CNPJ inválido: {e}")

        return cnpj

    def clean_telefone(self):
        """Validação do telefone"""
        telefone = self.cleaned_data.get("telefone")

        if telefone:
            telefone = telefone.strip()

            # Remove todos os caracteres não numéricos
            telefone_digits = "".join(filter(str.isdigit, telefone))

            if len(telefone_digits) != 10:
                raise ValidationError(
                    "O telefone deve ter 10 dígitos (ex: 1133334444)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = telefone_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

        return telefone

    def clean_whatsapp(self):
        """Validação do WhatsApp"""
        whatsapp = self.cleaned_data.get("whatsapp")

        if whatsapp:
            whatsapp = whatsapp.strip()

            # Remove todos os caracteres não numéricos
            whatsapp_digits = "".join(filter(str.isdigit, whatsapp))

            if len(whatsapp_digits) != 11:
                raise ValidationError(
                    "O WhatsApp deve ter 11 dígitos (ex: 11999999999)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = whatsapp_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

        return whatsapp

    def clean_email(self):
        """Validação do email"""
        email = self.cleaned_data.get("email")

        if email:
            email = email.strip().lower()

            if len(email) > 254:
                raise ValidationError("O email deve ter no máximo 254 caracteres.")

            # Verificar formato do email
            import re

            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, email):
                raise ValidationError("Digite um email válido.")

        return email

    def clean_cep(self):
        """Validação do CEP"""
        cep = self.cleaned_data.get("cep")

        if cep:
            cep = cep.strip()

            # Remove todos os caracteres não numéricos
            cep_digits = "".join(filter(str.isdigit, cep))

            if len(cep_digits) != 8:
                raise ValidationError("O CEP deve ter 8 dígitos.")

        return cep


class ProfileForm(forms.ModelForm):
    """Formulário para perfil do usuário"""

    class Meta:
        model = Profile
        fields = [
            "cpf",
            "telefone",
            "whatsapp",
            "data_nascimento",
            "avatar",
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
        ]
        widgets = {
            "cpf": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "000.000.000-00"}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 0000-0000"}
            ),
            "whatsapp": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 00000-0000"}
            ),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "cep": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "00000-000"}
            ),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "2"}
            ),
        }

    def clean_cpf(self):
        """Validação do CPF"""
        cpf = self.cleaned_data.get("cpf")

        if cpf:
            cpf = cpf.strip()

            # Remove todos os caracteres não numéricos
            cpf_digits = "".join(filter(str.isdigit, cpf))

            if len(cpf_digits) != 11:
                raise ValidationError("O CPF deve ter 11 dígitos.")

            # Verificar se não é uma sequência de números iguais
            if cpf_digits == cpf_digits[0] * 11:
                raise ValidationError("CPF inválido.")

            try:
                validate_cpf(cpf)
            except ValidationError as e:
                raise ValidationError(f"CPF inválido: {e}")

        return cpf

    def clean_telefone(self):
        """Validação do telefone"""
        telefone = self.cleaned_data.get("telefone")

        if telefone:
            telefone = telefone.strip()

            # Remove todos os caracteres não numéricos
            telefone_digits = "".join(filter(str.isdigit, telefone))

            if len(telefone_digits) != 10:
                raise ValidationError(
                    "O telefone deve ter 10 dígitos (ex: 1133334444)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = telefone_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

        return telefone

    def clean_whatsapp(self):
        """Validação do WhatsApp"""
        whatsapp = self.cleaned_data.get("whatsapp")

        if whatsapp:
            whatsapp = whatsapp.strip()

            # Remove todos os caracteres não numéricos
            whatsapp_digits = "".join(filter(str.isdigit, whatsapp))

            if len(whatsapp_digits) != 11:
                raise ValidationError(
                    "O WhatsApp deve ter 11 dígitos (ex: 11999999999)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = whatsapp_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

        return whatsapp

    def clean_data_nascimento(self):
        """Validação da data de nascimento"""
        data_nascimento = self.cleaned_data.get("data_nascimento")

        if data_nascimento:
            from datetime import date

            if data_nascimento > date.today():
                raise ValidationError("A data de nascimento não pode ser no futuro.")

            # Verificar se a pessoa tem pelo menos 13 anos
            idade = date.today().year - data_nascimento.year
            if idade < 13:
                raise ValidationError(
                    "Você deve ter pelo menos 13 anos para se cadastrar."
                )

        return data_nascimento

    def clean_cep(self):
        """Validação do CEP"""
        cep = self.cleaned_data.get("cep")

        if cep:
            cep = cep.strip()

            # Remove todos os caracteres não numéricos
            cep_digits = "".join(filter(str.isdigit, cep))

            if len(cep_digits) != 8:
                raise ValidationError("O CEP deve ter 8 dígitos.")

        return cep


class UserProfileForm(forms.ModelForm):
    """Formulário para dados básicos do usuário"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "data-mask": "(00) 00000-0000"}
            ),
        }

    def clean_first_name(self):
        """Validação do primeiro nome"""
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise ValidationError("O primeiro nome é obrigatório.")

        first_name = first_name.strip()

        if len(first_name) < 2:
            raise ValidationError("O primeiro nome deve ter pelo menos 2 caracteres.")

        if len(first_name) > 150:
            raise ValidationError("O primeiro nome deve ter no máximo 150 caracteres.")

        # Verificar caracteres válidos
        import re

        if not re.match(
            r"^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$", first_name
        ):
            raise ValidationError(
                "O primeiro nome deve conter apenas letras e espaços."
            )

        return first_name

    def clean_last_name(self):
        """Validação do sobrenome"""
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise ValidationError("O sobrenome é obrigatório.")

        last_name = last_name.strip()

        if len(last_name) < 2:
            raise ValidationError("O sobrenome deve ter pelo menos 2 caracteres.")

        if len(last_name) > 150:
            raise ValidationError("O sobrenome deve ter no máximo 150 caracteres.")

        # Verificar caracteres válidos
        import re

        if not re.match(
            r"^[a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]+$", last_name
        ):
            raise ValidationError("O sobrenome deve conter apenas letras e espaços.")

        return last_name

    def clean_email(self):
        """Validação do email"""
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError("O email é obrigatório.")

        email = email.strip().lower()

        if len(email) > 254:
            raise ValidationError("O email deve ter no máximo 254 caracteres.")

        # Verificar formato do email
        import re

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValidationError("Digite um email válido.")

        # Verificar se o email já existe para outro usuário
        if (
            User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("Este email já está em uso por outro usuário.")

        return email

    def clean_phone(self):
        """Validação do telefone"""
        phone = self.cleaned_data.get("phone")

        if phone:
            phone = phone.strip()

            # Remove todos os caracteres não numéricos
            phone_digits = "".join(filter(str.isdigit, phone))

            if len(phone_digits) != 11:
                raise ValidationError(
                    "O telefone deve ter 11 dígitos (ex: 11999999999)."
                )

            # Verificar se o DDD é válido (11-99)
            ddd = phone_digits[:2]
            if not (11 <= int(ddd) <= 99):
                raise ValidationError("DDD inválido.")

            # Verificar se o número não é sequencial
            if phone_digits == phone_digits[0] * 11:
                raise ValidationError("Número de telefone inválido.")

        return phone


class ChangePasswordForm(forms.Form):
    """Formulário para alteração de senha"""

    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Senha atual"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nova senha"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmar nova senha"}
        )
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        """Validação da senha atual"""
        current_password = self.cleaned_data.get("current_password")

        if not current_password:
            raise ValidationError("A senha atual é obrigatória.")

        if not self.user.check_password(current_password):
            raise ValidationError("Senha atual incorreta.")

        return current_password

    def clean_new_password1(self):
        """Validação da nova senha"""
        new_password1 = self.cleaned_data.get("new_password1")

        if not new_password1:
            raise ValidationError("A nova senha é obrigatória.")

        if len(new_password1) < 8:
            raise ValidationError("A nova senha deve ter pelo menos 8 caracteres.")

        if len(new_password1) > 128:
            raise ValidationError("A nova senha deve ter no máximo 128 caracteres.")

        # Verificar se a senha não é muito simples
        import re

        if not re.search(r"[A-Z]", new_password1):
            raise ValidationError(
                "A nova senha deve conter pelo menos uma letra maiúscula."
            )

        if not re.search(r"[a-z]", new_password1):
            raise ValidationError(
                "A nova senha deve conter pelo menos uma letra minúscula."
            )

        if not re.search(r"[0-9]", new_password1):
            raise ValidationError("A nova senha deve conter pelo menos um número.")

        # Verificar se a nova senha não é igual à senha atual
        if self.user.check_password(new_password1):
            raise ValidationError("A nova senha deve ser diferente da senha atual.")

        return new_password1

    def clean_new_password2(self):
        """Validação da confirmação da nova senha"""
        new_password2 = self.cleaned_data.get("new_password2")

        if not new_password2:
            raise ValidationError("A confirmação da nova senha é obrigatória.")

        return new_password2

    def clean(self):
        """Validação cruzada"""
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise ValidationError("As senhas não coincidem.")

        return cleaned_data

    def save(self):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user
