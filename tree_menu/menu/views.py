from django.shortcuts import render
from .models import MenuItem
from .templatetags.menu_tags import draw_menu
from django.core.cache import cache


def homepage_view(request):
    parent_items = MenuItem.objects.filter(parent__isnull=True).order_by('title')
    parent_data = {}

    for parent_item in parent_items:
        cached_data = cache.get(parent_item.menu_name)
        if cached_data:
            parent_data[parent_item] = cached_data
        else:
            menu_data = draw_menu(parent_item.menu_name)
            parent_data[parent_item] = menu_data
            cache.set(parent_item.menu_name, menu_data)

    context = {
        'parent_data': parent_data,
    }

    return render(request, 'menu/home.html', context)


def menu_view(request, menu_name):
    return render(request, 'menu/menu.html', {'menu_name': menu_name})
