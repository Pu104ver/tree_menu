from django import template
from django.core.cache import cache

from menu.models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name):
    """
    Функция для отрисовки меню на основе указанного имени меню.

    :param menu_name: Имя меню, которое нужно отрисовать.
    :return:
        dict: {
        'menu_name': имя переданного меню,
        'menu_html': html разметка меню
        }
    """
    cache_key = f"menu_html_{menu_name}"
    cached_menu_html = cache.get(cache_key)

    if cached_menu_html:
        return {'menu_name': menu_name, 'menu_html': cached_menu_html}

    try:
        menu = MenuItem.objects.select_related('parent').filter(menu_name=menu_name).first()
        if not menu:
            return {
                'menu_name': menu_name,
                'expanded_menu_html': 'Нет доступных пунктов меню'
            }

    except Exception:
        return {
            'menu_name': menu_name,
            'expanded_menu_html': 'Ошибка загрузки меню'
        }

    def generate_menu_html(expand_items, children_list: list, main_menu: MenuItem):
        menu_html = "<ul class='nav-tabs'>"
        if expand_items:
            for item, item_children in expand_items.items():
                if item == main_menu:
                    menu_html += (f"<li class='nav-item'><a class='nav-link' href='{item.url}'>"
                                  f"<strong>{item.title} (ТЕКУЩЕЕ)∇</strong></a>")
                    menu_html += "<ul class='nav flex-column ml-3'>"
                    for child in children_list:
                        menu_html += (f"<li class='nav-item'>"
                                      f"<a class='nav-link' href='{child.url}'>{child.title}</a></li>")
                    menu_html += "</ul>"
                else:
                    menu_html += f"<li class='nav-item'><a class='nav-link' href='{item.url}'>{item.title}</a>"
                if item_children:
                    menu_html += generate_menu_html(item_children, children_list, main_menu)
                menu_html += "</li>"
        else:
            if children_list:
                if main_menu:
                    menu_html += (f"<li class='nav-item'>"
                                  f"<a class='nav-link' href='{main_menu.url}'>{main_menu.title}∇</a></li>")
                    menu_html += "<ul class='nav flex-column ml-3'>"
                    for child in children_list:
                        menu_html += (f"<li class='nav-item'>"
                                      f"<a class='nav-link' href='{child.url}'>{child.title}</a></li>")
                    menu_html += "</ul>"
                else:
                    menu_html += "<li class='nav-item'>Не удалось обработать переданное меню</li>"

            else:
                menu_html += "<li>Нет доступных пунктов меню</li>"
        menu_html += "</ul>"
        return menu_html

    def get_expanded_items(menu_item: MenuItem) -> dict:
        above_items: dict = {}
        while menu_item:
            menu_item: MenuItem = menu_item.parent

            if menu_item and not menu_item.parent:
                expand_children = menu_item.get_children(main_menu=menu, all_children=True)
                above_items[menu_item] = expand_children

        return above_items

    children_items = []
    expanded_items = {}

    children = menu.get_children()

    if children:
        children_items.extend(children)

    if menu.parent:
        expanded_items = get_expanded_items(menu)

    menu_html_view = generate_menu_html(expand_items=expanded_items, children_list=children_items, main_menu=menu)
    cache.set(cache_key, menu_html_view, timeout=600)

    return {
        'menu_name': menu_name,
        'menu_html': menu_html_view
    }
