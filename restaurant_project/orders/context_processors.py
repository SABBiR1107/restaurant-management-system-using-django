def cart_item_count(request):
    """Context processor to add cart item count to all templates"""
    if request.user.is_authenticated:
        try:
            from .models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                return {'cart_item_count': cart.total_items}
        except:
            pass
    return {'cart_item_count': 0}
