from django.core.management.base import BaseCommand
from apps.authentication.models import User


class Command(BaseCommand):
    help = "Cria um superusuário para o VendaSimples"

    def handle(self, *args, **options):
        # Dados do superusuário
        email = "admin@vendefacil.com"
        first_name = "Carlos"
        last_name = "Alberto"
        password = "admin123"
        role = "SUPER"

        # Verificar se já existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"Usuário com email {email} já existe!")
            )
            return

        try:
            # Criar superusuário
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                password=password,
                is_staff=True,
                is_superuser=True,
                is_verified=True,
            )

            self.stdout.write(self.style.SUCCESS("✅ Superusuário criado com sucesso!"))
            self.stdout.write(f"📧 Email: {email}")
            self.stdout.write(f"🔑 Senha: {password}")
            self.stdout.write(f"👤 Nome: {user.get_full_name()}")
            self.stdout.write(f"🎭 Função: {user.get_role_display()}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao criar superusuário: {e}"))
