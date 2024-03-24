from django.core.cache import cache
from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=100, default='TestTitle')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=200, default='/menu/test')
    menu_name = models.CharField(max_length=50, default='test', unique=True)

    @staticmethod
    def check_for_menu(menu_dict: dict, main_menu: 'MenuItem') -> bool:
        """
        Проверяет, содержится ли главное меню в словаре меню.

        Args:
            menu_dict (dict): Словарь меню.
            main_menu (MenuItem): Главное меню для проверки.

        Returns:
            bool: True, если главное меню содержится в словаре, иначе False.
        """
        if not main_menu:
            return False
        if main_menu in menu_dict:
            return True
        else:
            for value in menu_dict.values():
                if isinstance(value, dict):
                    if MenuItem.check_for_menu(value, main_menu):
                        return True
        return False

    def get_children(self, first=False, main_menu=None, all_children=False) -> dict:
        """
        Получает дочерние элементы текущего меню.

        Args:
            first (bool): Флаг, указывающий, нужно ли получить только первого ребенка (для ограничения вывода потомков).
            main_menu (MenuItem): Главное меню.
            all_children (bool): Флаг, указывающий, нужно ли получить всех потомков.

        Returns:
            dict:
                Словарь дочерних элементов текущего меню:
                    Ключ - MenuItem (родительский элемент)
                    Значение - dict: {
                               Ключ - MenuItem (ребенок)
                               Значение - dict: Словарь дочерних элементов ребенка текущего меню (потомки ребенка)
                               }
        """
        cache_key = f"children_{self.pk}_{main_menu.pk if main_menu else 'None'}_{first}_{all_children}"
        cached_children = cache.get(cache_key)
        if cached_children:
            return cached_children

        children = list(self.children.all().order_by('title'))
        children_dict = {}

        if not children:
            return children_dict

        if not all_children:
            children_dict = {child: None for child in children}
            cache.set(cache_key, children_dict, timeout=600)
            return children_dict

        if first:
            children = children[:1]

        for child in children:
            # Если найдено "главное меню" - заносим в словарь и переходим к другим "детям"
            if child == main_menu:
                children_dict[child] = {}
                continue

            # Если "главное меню" найдено, то поиск потомков прекращается для оставшихся детей прекращается
            if self.check_for_menu(menu_dict=children_dict, main_menu=main_menu):
                # Заносим оставшихся детей с пустым словарем потомков (для ограничения "развертываемости")
                children_dict[child] = {}
                continue

            child_children = child.get_children(main_menu=main_menu, all_children=True)
            children_dict[child] = child_children

        cache.set(cache_key, children_dict, timeout=600)
        return children_dict

    def __str__(self):
        return self.title
