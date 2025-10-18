from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'name': ('name',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'preparation_time']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_spicy']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']