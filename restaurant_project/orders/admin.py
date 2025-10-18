from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    autocomplete_fields = ['user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'menu_item', 'quantity', 'total_price', 'created_at')
    search_fields = ('cart__user__username', 'menu_item__name')
    list_filter = ('menu_item',)
    ordering = ('-created_at',)
    autocomplete_fields = ['cart', 'menu_item']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'delivery_type', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'delivery_type', 'created_at')
    search_fields = ('order_number', 'user__username', 'special_instructions', 'delivery_address', 'table_number')
    ordering = ('-created_at',)
    autocomplete_fields = ['user']
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Delivery Information', {
            'fields': ('delivery_type', 'delivery_address', 'table_number')
        }),
        ('Additional Information', {
            'fields': ('special_instructions', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('order_number', 'created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price', 'total_price', 'special_instructions')
    search_fields = ('order__order_number', 'menu_item__name')
    list_filter = ('menu_item',)
    autocomplete_fields = ['order', 'menu_item']



