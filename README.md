# VendaSimples

Sistema completo de catálogo/vitrine de produtos desenvolvido com Django 5.0+.

## 🚀 Características

- **Sistema hierárquico de usuários**: Superusuário, Empresa, Vendedor
- **Gestão completa de produtos**: Upload de múltiplas imagens, categorias, variações
- **Catálogos públicos**: Personalizados por vendedor/empresa
- **Carrinho de compras**: Sessão e persistido
- **Sistema de pedidos**: Com máquina de estados
- **Múltiplos métodos de pagamento**: Dinheiro, cartão, PIX, etc.
- **Integração WhatsApp**: Para pedidos
- **Dashboards personalizados**: Por tipo de usuário
- **Sistema de notificações**: Multi-canal
- **API REST completa**: Com versionamento

## 🛠️ Tecnologias

- **Backend**: Django 5.0+
- **Banco de Dados**: PostgreSQL 14+
- **Cache**: Redis 7+
- **Frontend**: Bootstrap 5.3, JavaScript ES6+, jQuery
- **API**: Django REST Framework 3.14+
- **Task Queue**: Celery 5.3+
- **Storage**: AWS S3 (configurável para local)

## 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Node.js (para build de assets)

## 🔧 Instalação

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd vendefacil
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   # Crie o banco PostgreSQL
   createdb vendasimples
   ```

5. **Configure as variáveis de ambiente**
   ```bash
   cp env.example .env
   # Edite o arquivo .env com suas configurações
   ```

6. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

8. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

## 🗂️ Estrutura do Projeto

```
vendasimples/
├── config/                    # Configurações Django
├── apps/                      # Aplicações Django
│   ├── core/                  # Utilitários compartilhados
│   ├── authentication/        # Sistema de usuários
│   ├── produtos/              # Gestão de produtos
│   ├── pedidos/               # Sistema de pedidos
│   ├── carrinho/              # Carrinho de compras
│   ├── pagamento/             # Sistema de pagamentos
│   ├── catalogo/              # Catálogo público
│   ├── configuracoes/         # Configurações
│   ├── dashboard/             # Dashboards
│   ├── notificacoes/          # Notificações
│   ├── whatsapp/              # Integração WhatsApp
│   ├── estatisticas/          # Estatísticas
│   └── api/                   # API REST
├── templates/                 # Templates Django
├── static/                    # Arquivos estáticos
├── media/                     # Arquivos de mídia
└── docs/                      # Documentação
```

## 👥 Tipos de Usuário

### Superusuário
- Acesso total ao sistema
- Gerenciamento de todas as empresas e vendedores
- Configurações globais do sistema

### Empresa
- Gerenciamento de vendedores
- Visualização de produtos e pedidos
- Configurações da empresa

### Vendedor
- Gerenciamento de produtos
- Visualização de pedidos
- Configurações do perfil

## 🔌 API

A API REST está disponível em `/api/v1/` com documentação automática em `/api/docs/`.

### Endpoints principais:
- `GET /api/v1/produtos/` - Lista produtos
- `GET /api/v1/categorias/` - Lista categorias
- `GET /api/v1/pedidos/` - Lista pedidos
- `GET /api/v1/usuarios/` - Lista usuários
- `GET /api/v1/empresas/` - Lista empresas

## 🚀 Deploy

### Produção

1. **Configure as variáveis de ambiente para produção**
2. **Configure o banco de dados PostgreSQL**
3. **Configure Redis para cache**
4. **Configure Celery para tasks**
5. **Configure AWS S3 para storage (opcional)**
6. **Execute as migrações**
7. **Colete os arquivos estáticos**
8. **Configure o servidor web (Nginx + Gunicorn)**

### Docker (Opcional)

```bash
docker-compose up -d
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, envie um email para suporte@vendasimples.com.br ou abra uma issue no GitHub.

## 🔄 Changelog

### v1.0.0
- Sistema inicial completo
- Autenticação com roles
- Gestão de produtos
- Sistema de pedidos
- Carrinho de compras
- API REST
- Dashboards personalizados