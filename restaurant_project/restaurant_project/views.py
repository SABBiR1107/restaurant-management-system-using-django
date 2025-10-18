from django.shortcuts import render
from menu.models import MenuItem

def home(request):
    """Home page view with featured menu items"""
    featured_items = MenuItem.objects.filter(is_available=True)[:4]  # Get first 4 available items as featured
    context = {
        'featured_items': featured_items
    }
    return render(request, 'home.html', context)

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')
