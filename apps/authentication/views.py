"""
Views for authentication app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    EmpresaForm,
    ProfileForm,
    UserProfileForm,
    ChangePasswordForm,
)
from .models import User, Empresa, Profile, UserRole
from .decorators import role_required


class UserLoginView(LoginView):
    """View de login"""

    template_name = "authentication/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True
    authentication_form = UserLoginForm

    def get_success_url(self):
        """Redireciona baseado no papel do usuário"""
        user = self.request.user
        if user.role == UserRole.SUPERUSER:
            return reverse_lazy("admin:index")
        elif user.role == UserRole.EMPRESA:
            return reverse_lazy("dashboard:empresa")
        else:
            return reverse_lazy("dashboard:vendedor")

    def form_valid(self, form):
        """Autentica o usuário"""
        from django.contrib.auth import login

        user = form.get_user()

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            form.add_error(None, "Email/nome ou senha inválidos")
            return self.form_invalid(form)


class UserLogoutView(LogoutView):
    """View de logout"""

    next_page = reverse_lazy("authentication:login")


class UserRegistrationView(CreateView):
    """View de registro de usuário"""

    model = User
    form_class = UserRegistrationForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("authentication:login")

    def form_valid(self, form):
        """Processa registro bem-sucedido"""
        response = super().form_valid(form)

        # Criar perfil do usuário
        Profile.objects.create(user=self.object)

        messages.success(
            self.request, "Usuário criado com sucesso! Faça login para continuar."
        )
        return response


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    """View principal do dashboard"""

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Dados específicos por papel
        if user.role == UserRole.EMPRESA:
            context["empresa"] = user.empresa
            context["total_vendedores"] = user.empresa.total_vendedores
            context["total_produtos"] = user.empresa.total_produtos
        elif user.role == UserRole.VENDEDOR:
            context["total_produtos"] = user.produtos.count()
            context["total_pedidos"] = user.pedidos_vendedor.count()

        return context


@login_required
def profile_view(request):
    """View do perfil do usuário"""
    from .models import Profile

    user = request.user

    # Criar perfil se não existir
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("authentication:profile")
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "authentication/profile.html", context)


@role_required(["EMPRESA"])
@login_required
def empresa_settings_view(request):
    """View de configurações da empresa"""
    user = request.user
    empresa = user.empresa

    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações da empresa atualizadas!")
            return redirect("authentication:empresa_settings")
    else:
        form = EmpresaForm(instance=empresa)

    context = {
        "form": form,
        "empresa": empresa,
    }

    return render(request, "authentication/empresa_settings.html", context)


@login_required
def change_password_view(request):
    """View para alterar senha"""
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("authentication:profile")
    else:
        form = ChangePasswordForm(request.user)

    context = {
        "form": form,
    }

    return render(request, "authentication/change_password.html", context)


@csrf_exempt
def check_email_exists(request):
    """API para verificar se email existe"""
    if request.method == "POST":
        email = request.POST.get("email")
        exists = User.objects.filter(email__iexact=email).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def check_cpf_exists(request):
    """API para verificar se CPF existe"""
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        exists = Profile.objects.filter(cpf=cpf).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def check_cnpj_exists(request):
    """API para verificar se CNPJ existe"""
    if request.method == "POST":
        cnpj = request.POST.get("cnpj")
        exists = Empresa.objects.filter(cnpj=cnpj).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"error": "Method not allowed"}, status=405)
