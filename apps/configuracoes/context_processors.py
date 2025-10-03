"""
Context processors for configuracoes app.
"""

def configuracoes_site(request):
    """Adiciona configurações do site ao contexto"""
    # Aqui você pode adicionar configurações globais do site
    return {
        'site_name': 'VendaSimples',
        'site_description': 'Sistema de catálogo/vitrine de produtos',
    }
