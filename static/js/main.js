// Main JavaScript for VendaSimples

$(document).ready(function () {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function () {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Form validation
    $('form').on('submit', function (e) {
        var form = $(this);
        var submitBtn = form.find('button[type="submit"]');

        // Disable submit button to prevent double submission
        submitBtn.prop('disabled', true);

        // Re-enable after 3 seconds
        setTimeout(function () {
            submitBtn.prop('disabled', false);
        }, 3000);
    });

    // AJAX cart functions
    $('.add-to-cart').on('click', function (e) {
        e.preventDefault();

        var button = $(this);
        var productId = button.data('product-id');
        var quantity = button.siblings('input[name="quantidade"]').val() || 1;

        // Show loading state
        button.html('<span class="spinner"></span> Adicionando...');
        button.prop('disabled', true);

        $.ajax({
            url: '/carrinho/add/' + productId + '/',
            method: 'POST',
            data: {
                'quantidade': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                if (response.success) {
                    // Show success message
                    showAlert('success', response.message);

                    // Update cart counter if exists
                    if ($('.cart-counter').length) {
                        $('.cart-counter').text(response.cart_total);
                    }
                } else {
                    showAlert('danger', 'Erro ao adicionar produto ao carrinho');
                }
            },
            error: function () {
                showAlert('danger', 'Erro ao adicionar produto ao carrinho');
            },
            complete: function () {
                // Reset button state
                button.html('Adicionar ao Carrinho');
                button.prop('disabled', false);
            }
        });
    });

    // Remove from cart
    $('.remove-from-cart').on('click', function (e) {
        e.preventDefault();

        var button = $(this);
        var productId = button.data('product-id');

        if (confirm('Deseja remover este produto do carrinho?')) {
            $.ajax({
                url: '/carrinho/remove/' + productId + '/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                success: function (response) {
                    if (response.success) {
                        // Remove item from DOM
                        button.closest('.cart-item').fadeOut();

                        // Update cart total
                        if (response.cart_total == 0) {
                            $('.cart-content').html('<p class="text-center">Carrinho vazio</p>');
                        }

                        showAlert('success', response.message);
                    }
                }
            });
        }
    });

    // Update cart quantity
    $('.update-cart-quantity').on('change', function () {
        var input = $(this);
        var productId = input.data('product-id');
        var quantity = input.val();

        $.ajax({
            url: '/carrinho/update/' + productId + '/',
            method: 'POST',
            data: {
                'quantidade': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                if (response.success) {
                    // Update cart total
                    $('.cart-total').text('R$ ' + response.cart_price);
                    showAlert('success', response.message);
                }
            }
        });
    });

    // Image preview for file inputs
    $('input[type="file"]').on('change', function () {
        var input = this;
        var preview = $(input).siblings('.image-preview');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                preview.attr('src', e.target.result).show();
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    // Phone mask
    if (typeof $.fn.mask !== 'undefined') {
        $('input[data-mask="(00) 0000-0000"]').mask('(00) 0000-0000');
        $('input[data-mask="(00) 00000-0000"]').mask('(00) 00000-0000');

        // CPF mask
        $('input[data-mask="000.000.000-00"]').mask('000.000.000-00');

        // CNPJ mask
        $('input[data-mask="00.000.000/0000-00"]').mask('00.000.000/0000-00');

        // CEP mask
        $('input[data-mask="00000-000"]').mask('00000-000');
    } else {
        console.warn('jQuery Mask Plugin não foi carregado');
    }

    // CEP lookup
    $('input[data-mask="00000-000"]').on('blur', function () {
        var cep = $(this).val().replace(/\D/g, '');

        if (cep.length === 8) {
            $.get('https://viacep.com.br/ws/' + cep + '/json/', function (data) {
                if (!data.erro) {
                    $('input[name="endereco"]').val(data.logradouro);
                    $('input[name="bairro"]').val(data.bairro);
                    $('input[name="cidade"]').val(data.localidade);
                    $('input[name="estado"]').val(data.uf);
                }
            });
        }
    });
});

// Utility functions
function showAlert(type, message) {
    var alertHtml = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
        '</div>';

    $('.container-fluid').prepend(alertHtml);

    // Auto-hide after 3 seconds
    setTimeout(function () {
        $('.alert').fadeOut('slow');
    }, 3000);
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}

// Export functions for global use
window.VendaSimples = {
    showAlert: showAlert,
    formatCurrency: formatCurrency,
    formatDate: formatDate
};
