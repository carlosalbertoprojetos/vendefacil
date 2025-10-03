/**
 * Sistema de Mensagens com Modais Bootstrap
 * Facilita a exibição de mensagens, alertas e notificações em modais
 */

// Aguardar o carregamento do DOM
document.addEventListener('DOMContentLoaded', function () {

    // Função para exibir mensagem de sucesso
    window.showSuccess = function (message, title = 'Sucesso!', options = {}) {
        if (typeof showSuccessMessage === 'function') {
            showSuccessMessage(title, message, options);
        } else {
            console.warn('showSuccessMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para exibir mensagem de erro
    window.showError = function (message, title = 'Erro!', options = {}) {
        if (typeof showErrorMessage === 'function') {
            showErrorMessage(title, message, options);
        } else {
            console.warn('showErrorMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para exibir mensagem de aviso
    window.showWarning = function (message, title = 'Atenção!', options = {}) {
        if (typeof showWarningMessage === 'function') {
            showWarningMessage(title, message, options);
        } else {
            console.warn('showWarningMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para exibir mensagem informativa
    window.showInfo = function (message, title = 'Informação', options = {}) {
        if (typeof showInfoMessage === 'function') {
            showInfoMessage(title, message, options);
        } else {
            console.warn('showInfoMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para exibir confirmação
    window.showConfirm = function (message, title = 'Confirmação', onConfirm = null, onCancel = null) {
        if (typeof showUnifiedMessage === 'function') {
            showUnifiedMessage('warning', title, message, {
                buttonText: 'Cancelar',
                buttonIcon: 'fas fa-times',
                buttonClass: 'btn-secondary',
                extraButtons: [
                    {
                        text: 'Confirmar',
                        class: 'btn-warning',
                        icon: 'fas fa-check',
                        onclick: function () {
                            if (onConfirm) onConfirm();
                            bootstrap.Modal.getInstance(document.getElementById('unifiedMessageModal')).hide();
                        }
                    }
                ]
            });
        } else {
            console.warn('showUnifiedMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para exibir loading
    window.showLoading = function (message = 'Carregando...', title = 'Aguarde') {
        if (typeof showUnifiedMessage === 'function') {
            showUnifiedMessage('info', title, message, {
                buttonText: 'Cancelar',
                buttonIcon: 'fas fa-times',
                buttonClass: 'btn-secondary',
                icon: 'fas fa-spinner fa-spin'
            });
        } else {
            console.warn('showUnifiedMessage não está disponível. Certifique-se de incluir _unified_modal.html');
        }
    };

    // Função para esconder loading
    window.hideLoading = function () {
        const modal = bootstrap.Modal.getInstance(document.getElementById('unifiedMessageModal'));
        if (modal) {
            modal.hide();
        }
    };

    // Função para exibir erro de validação de formulário
    window.showFormErrors = function (errors, title = 'Erro na validação') {
        let message = 'Por favor, corrija os seguintes erros:';

        if (typeof errors === 'object') {
            message += '<ul class="mb-0 mt-2">';
            Object.keys(errors).forEach(function (field) {
                const fieldErrors = errors[field];
                fieldErrors.forEach(function (error) {
                    message += '<li><strong>' + field + ':</strong> ' + error + '</li>';
                });
            });
            message += '</ul>';
        } else if (typeof errors === 'string') {
            message = errors;
        }

        showError(message, title);
    };

    // Função para exibir erro de API
    window.showApiError = function (error, title = 'Erro na comunicação') {
        let message = 'Ocorreu um erro na comunicação com o servidor.';

        if (error && error.message) {
            message = error.message;
        } else if (error && error.detail) {
            message = error.detail;
        } else if (typeof error === 'string') {
            message = error;
        }

        showError(message, title, {
            extraButtons: [
                {
                    text: 'Tentar Novamente',
                    class: 'btn-outline-danger',
                    icon: 'fas fa-redo',
                    onclick: function () {
                        location.reload();
                    }
                }
            ]
        });
    };

    // Interceptar erros de fetch para exibir automaticamente
    const originalFetch = window.fetch;
    window.fetch = function (...args) {
        return originalFetch.apply(this, args)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição: ' + response.status);
                }
                return response;
            })
            .catch(error => {
                console.error('Erro de fetch:', error);
                showApiError(error);
                throw error;
            });
    };

    // Interceptar erros de JavaScript não tratados
    window.addEventListener('error', function (event) {
        console.error('Erro JavaScript:', event.error);
        showError('Ocorreu um erro inesperado. Por favor, recarregue a página e tente novamente.', 'Erro no sistema', {
            extraButtons: [
                {
                    text: 'Recarregar Página',
                    class: 'btn-outline-danger',
                    icon: 'fas fa-refresh',
                    onclick: function () {
                        location.reload();
                    }
                }
            ]
        });
    });

    // Interceptar promessas rejeitadas não tratadas
    window.addEventListener('unhandledrejection', function (event) {
        console.error('Promessa rejeitada:', event.reason);
        showError('Ocorreu um erro na comunicação com o servidor. Por favor, tente novamente.', 'Erro de comunicação');
    });

    // Exemplos de uso (comentados):
    /*
    // Mensagens simples
    showSuccess('Operação realizada com sucesso!');
    showError('Ocorreu um erro inesperado.');
    showWarning('Verifique os dados informados.');
    showInfo('Esta é uma mensagem informativa.');
    
    // Confirmação
    showConfirm('Deseja realmente excluir este item?', 'Confirmar exclusão', function() {
        console.log('Usuário confirmou');
    });
    
    // Loading
    showLoading('Processando dados...');
    // ... fazer alguma operação ...
    hideLoading();
    
    // Erros de formulário
    showFormErrors({
        'nome': ['Este campo é obrigatório'],
        'email': ['Email inválido']
    });
    
    // Erro de API
    showApiError('Erro ao salvar dados');
    */
});
