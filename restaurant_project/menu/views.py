from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, MenuItem

def menu_list(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('menu_items')
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    
    menu_items = MenuItem.objects.filter(is_available=True)
    
    if query:
        menu_items = menu_items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_filter:
        menu_items = menu_items.filter(category_id=category_filter)
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'search_query': query,
        'selected_category': category_filter,
    }
    return render(request, 'menu/menu_list.html', context)

def menu_item_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk, is_available=True)
    related_items = MenuItem.objects.filter(
        category=menu_item.category, 
        is_available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'menu_item': menu_item,
        'related_items': related_items,
    }
    return render(request, 'menu/menu_item_detail.html', context)