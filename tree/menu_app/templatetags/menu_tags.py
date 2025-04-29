from django import template

from menu_app.models import Menu


register = template.Library()


@register.inclusion_tag("menu_app/menu.html", takes_context=True)
def draw_menu(context, menu_name) -> dict:
    """
    Функция для рисования меню на основе переданного имени меню.
    Она получает контекст и имя меню, а затем возвращает словарь с информацией о меню,
    включая дерево меню, активный путь и текущий запрос.
    """
    
    request = context["request"]
    current_path = request.path

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {"menu_items": []}

    items = menu.items.select_related("parent").all()

    tree = []
    lookup = {}

    for item in items:
        lookup[item.id] = {"item": item, "children": []}

    for node in lookup.values():
        item = node["item"]
        if item.parent_id:
            parent_node = lookup.get(item.parent_id)
            if parent_node:
                parent_node["children"].append(node)
        else:
            tree.append(node)

    active_item = None
    for item in items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    active_path = set()

    def build_active_path(item):
        while item:
            active_path.add(item.id)
            item = item.parent

    if active_item:
        build_active_path(active_item)

    return {
        "tree": tree,
        "active_path": active_path,
        "request": request,
    }
