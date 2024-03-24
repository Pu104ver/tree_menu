from django import template

from menu.models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name, only_children=False):
    def generate_menu_html(expand_items, children_list: list, main_menu: MenuItem):
        menu_html = "<ul>"
        if expand_items:
            menu_html += "<li>Обнаружен экспанд</li>"

            for item, children in expand_items.items():
                if item == main_menu:
                    menu_html += f"<li><a href='{item.url}'><strong>{item.title} (ТЕКУЩЕЕ)</strong></a>"
                    menu_html += "<ul>"
                    for child in children_list:
                        menu_html += f"<li><a href='{child.url}'>{child.title} (дочернее меню)</a></li>"
                    menu_html += "</ul>"
                else:
                    menu_html += f"<li><a href='{item.url}'>{item.title}</a>"
                if children:
                    menu_html += generate_menu_html(children, children_list, main_menu)
                menu_html += "</li>"
        else:
            menu_html += "<li>Не Обнаружен экспанд</li>"

            if children_list:
                menu_html += "<li>Обнаружен детский дом</li>"

                if main_menu:
                    menu_html += f"<li><a href='{main_menu.url}'>{main_menu.title}</a></li>"
                    menu_html += "<ul>"
                    for child in children_list:
                        menu_html += f"<li><a href='{child.url}'>{child.title} (дочернее меню)</a></li>"
                    menu_html += "</ul>"
                else:
                    menu_html += "<li>Не удалось обработать переданное меню</li>"

            else:
                menu_html += "<li>Нет доступных пунктов меню</li>"
        menu_html += "</ul>"
        return menu_html

    menu: MenuItem = MenuItem.objects.select_related('parent').filter(menu_name=menu_name).first()
    if not menu:
        return {'expanded_menu_html': 'Нет доступных пунктов меню'}

    def get_expanded_items(item: MenuItem) -> dict:
        above_items: dict = {}
        while item:
            item = item.parent
            if item and not item.parent:
                expand_children = item.get_all_children(main_menu=menu)
                above_items[item] = expand_children

        return above_items

    children_items = []
    expanded_items = {}

    children = menu.get_children()

    if children:
        children_items.extend(children)

    if menu.parent:
        expanded_items = get_expanded_items(menu)

    expanded_menu_html = generate_menu_html(expanded_items, children_items, menu)

    return {
        'main_menu': menu_name,
        'child_menu': children_items,
        'expanded_items': expanded_items,
        'expanded_menu_html': expanded_menu_html
    }
