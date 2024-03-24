from django.shortcuts import render
from .models import MenuItem
from .templatetags.menu_tags import draw_menu


def homepage_view(request):
    parent_items: list['MenuItem'] = MenuItem.objects.filter(parent__isnull=True)

    parent_data = {}

    for parent_item in parent_items:
        menu_data = draw_menu(parent_item.menu_name)
        parent_data[parent_item] = menu_data

    context = {
        'parent_data': parent_data,
    }

    return render(request, 'menu/home.html', context)


def menu_view(request, menu_name):
    menu_data = draw_menu(menu_name)
    return render(request, 'menu/menu.html', {'menu_data': menu_data})
    # menu_items = MenuItem.objects.filter(menu_name=menu_name)
