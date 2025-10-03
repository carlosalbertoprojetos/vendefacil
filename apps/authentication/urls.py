"""
URLs for authentication app.
"""

from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Company settings
    path('empresa/settings/', views.empresa_settings_view, name='empresa_settings'),
    
    # API endpoints
    path('api/check-email/', views.check_email_exists, name='check_email'),
    path('api/check-cpf/', views.check_cpf_exists, name='check_cpf'),
    path('api/check-cnpj/', views.check_cnpj_exists, name='check_cnpj'),
]
