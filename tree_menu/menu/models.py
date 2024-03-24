from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=100, default='TestTitle')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=200, default='/menu/test')
    menu_name = models.CharField(max_length=50, default='test', unique=True)

    @staticmethod
    def check_for_menu(menu_dict: dict, main_menu: 'MenuItem') -> bool:
        if main_menu in menu_dict:
            return True
        else:
            for value in menu_dict.values():
                if isinstance(value, dict):
                    if MenuItem.check_for_menu(value, main_menu):
                        return True
        return False

    def get_children(self) -> list['MenuItem']:
        # children: List['MenuItem'] = list(MenuItem.objects.filter(parent=self))
        children = list(MenuItem.objects.filter(parent=self).order_by('menu_name'))

        return children

    def get_all_children(self, main_menu=None) -> dict:
        children_dict = {}
        children = list(MenuItem.objects.filter(parent=self).order_by('menu_name'))
        # children = list(MenuItem.objects.filter(parent=self))

        for child in children:
            if self.check_for_menu(children_dict, main_menu):
                return children_dict


            if main_menu and child == main_menu:
                children_dict[child] = {}
                return children_dict

            child_children = child.get_all_children(main_menu)
            children_dict[child] = child_children

        return children_dict

    def __str__(self):
        return self.title
