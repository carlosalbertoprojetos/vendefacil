"""
Custom managers for authentication models.
"""

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager customizado para o modelo User"""

    def create_user(
        self, email, first_name, last_name, role, password=None, **extra_fields
    ):
        """Cria um usuário comum"""
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        """Cria um superusuário"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "SUPER")
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True")

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

    def get_by_natural_key(self, username):
        """Permite login com email ou nome completo"""
        # Tenta primeiro por email
        try:
            return self.get(email__iexact=username)
        except self.model.DoesNotExist:
            # Se não encontrar por email, tenta por nome completo
            try:
                return self.get(first_name__iexact=username)
            except self.model.DoesNotExist:
                # Se não encontrar por nome, tenta por nome completo (first_name + last_name)
                try:
                    return self.get(
                        first_name__iexact=username.split()[0],
                        last_name__iexact=username.split()[-1],
                    )
                except (self.model.DoesNotExist, IndexError):
                    # Se não encontrar, levanta a exceção original
                    raise self.model.DoesNotExist

    def active(self):
        """Retorna apenas usuários ativos"""
        return self.filter(is_active=True, deleted_at__isnull=True)

    def verified(self):
        """Retorna apenas usuários verificados"""
        return self.filter(is_verified=True)

    def by_role(self, role):
        """Retorna usuários por função"""
        return self.filter(role=role)

    def authenticate_user(self, username, password):
        """Autentica usuário por email ou nome"""
        from django.contrib.auth.hashers import check_password

        # Tenta encontrar o usuário por email ou nome
        user = None
        try:
            # Primeiro tenta por email
            user = self.get(email__iexact=username)
        except self.model.DoesNotExist:
            try:
                # Tenta por nome completo (first_name + last_name)
                if " " in username:
                    first_name, last_name = username.split(" ", 1)
                    user = self.get(
                        first_name__iexact=first_name, last_name__iexact=last_name
                    )
                else:
                    # Tenta apenas por first_name
                    user = self.get(first_name__iexact=username)
            except self.model.DoesNotExist:
                pass

        if user and user.check_password(password) and user.is_active:
            return user
        return None
