// AJAX Add to Cart
$(document).ready(function() {
    // Add to cart with AJAX
    $('.add-to-cart-form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var button = form.find('button');
        var originalText = button.html();
        
        button.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Adding...');
        
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    // Update cart badge
                    var cartBadge = $('.cart-badge');
                    cartBadge.text(response.cart_total_items);
                    
                    // Show or hide badge based on count
                    if (response.cart_total_items > 0) {
                        cartBadge.show();
                    } else {
                        cartBadge.hide();
                    }
                    
                    // Show success message
                    showToast('Success', response.message, 'success');
                }
            },
            error: function() {
                showToast('Error', 'Failed to add item to cart', 'error');
            },
            complete: function() {
                button.prop('disabled', false).html(originalText);
            }
        });
    });
    
    // Quantity controls
    $('.quantity-btn').on('click', function() {
        var input = $(this).siblings('.quantity-input');
        var currentVal = parseInt(input.val());
        
        if ($(this).hasClass('increase')) {
            input.val(currentVal + 1);
        } else if ($(this).hasClass('decrease') && currentVal > 1) {
            input.val(currentVal - 1);
        }
        
        input.trigger('change');
    });
});

function showToast(title, message, type) {
    // Simple toast notification
    var toast = $(`
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0 position-fixed top-0 end-0 m-3" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}:</strong> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);
    
    $('body').append(toast);
    var bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

// Auto-hide alerts after 5 seconds
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
    
    // Update cart count on page load (in case it changed)
    updateCartCount();
});

function updateCartCount() {
    // This function can be called to refresh the cart count
    // For now, we rely on the context processor to provide the correct count
    // In the future, this could make an AJAX call to get the latest count
}