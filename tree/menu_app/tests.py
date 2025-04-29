from django.test import TestCase

from menu_app.models import Menu, MenuItem

class MenuTestCase(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="main_menu")
        self.parent_item = MenuItem.objects.create(
            menu=self.menu,
            title="Главная",
            url="/",
            parent=None
        )
        self.child_item = MenuItem.objects.create(
            menu=self.menu,
            title="О нас",
            url="/about/",
            parent=self.parent_item
        )

    def test_menu_exists(self):
        self.assertEqual(Menu.objects.count(), 1)

    def test_menu_item_structure(self):
        self.assertEqual(self.parent_item.children.count(), 1)
        self.assertEqual(self.child_item.parent, self.parent_item)

    def test_menu_view_rendering(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Главная")
