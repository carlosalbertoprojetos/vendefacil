"""
Constants for VendaSimples project.
"""

# User Roles
USER_ROLES = {
    'SUPERUSER': 'SUPER',
    'EMPRESA': 'EMPRESA',
    'VENDEDOR': 'VENDEDOR',
}

# Order Status
ORDER_STATUS = {
    'PENDENTE': 'PENDENTE',
    'CONFIRMADO': 'CONFIRMADO',
    'PREPARANDO': 'PREPARANDO',
    'PRONTO': 'PRONTO',
    'SAIU_ENTREGA': 'SAIU_ENTREGA',
    'ENTREGUE': 'ENTREGUE',
    'CANCELADO': 'CANCELADO',
}

# Payment Methods
PAYMENT_METHODS = {
    'DINHEIRO': 'DINHEIRO',
    'CARTAO_CREDITO': 'CARTAO_CREDITO',
    'CARTAO_DEBITO': 'CARTAO_DEBITO',
    'PIX': 'PIX',
    'TRANSFERENCIA': 'TRANSFERENCIA',
    'BOLETO': 'BOLETO',
}

# Payment Status
PAYMENT_STATUS = {
    'PENDENTE': 'PENDENTE',
    'PROCESSANDO': 'PROCESSANDO',
    'APROVADO': 'APROVADO',
    'REJEITADO': 'REJEITADO',
    'CANCELADO': 'CANCELADO',
    'ESTORNADO': 'ESTORNADO',
}

# Notification Channels
NOTIFICATION_CHANNELS = {
    'EMAIL': 'EMAIL',
    'SMS': 'SMS',
    'WHATSAPP': 'WHATSAPP',
    'PUSH': 'PUSH',
}

# File Upload Limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']

# Cache Keys
CACHE_KEYS = {
    'USER_PROFILE': 'user_profile_{user_id}',
    'PRODUCT_LIST': 'product_list_{seller_id}_{page}',
    'CATEGORY_LIST': 'category_list',
    'SITE_CONFIG': 'site_config',
}

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
