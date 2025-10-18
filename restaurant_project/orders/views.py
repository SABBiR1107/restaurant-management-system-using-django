from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from menu.models import MenuItem

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@require_POST
@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{menu_item.name} added to cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_items,
            'message': f'{menu_item.name} added to cart!'
        })
    
    return redirect('menu_list')

@require_POST
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart_view')

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart_view')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.total_items == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('menu_list')
    
    if request.method == 'POST':
        delivery_type = request.POST.get('delivery_type', 'dine_in')
        delivery_address = request.POST.get('delivery_address', '')
        table_number = request.POST.get('table_number', '')
        special_instructions = request.POST.get('special_instructions', '')
        
        # Validate required fields based on delivery type
        if delivery_type == 'takeaway' and not delivery_address.strip():
            messages.error(request, 'Please provide a delivery address for takeaway orders.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        if delivery_type == 'dine_in' and not table_number.strip():
            messages.error(request, 'Please provide a table number for dine-in orders.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            delivery_type=delivery_type,
            delivery_address=delivery_address,
            table_number=table_number,
            total_amount=cart.total_price,
            special_instructions=special_instructions
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price,
                special_instructions=cart_item.special_instructions
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('order_history')
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
