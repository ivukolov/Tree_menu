from django.test import TestCase, Client
from django.shortcuts import reverse
from menu.models import MenuItem



class MenuCreationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu_name =  'main_menu'
        cls.data = {
            'main_data': ('Главная', 'home'),
            'about_data': ('О нас', 'about'),
            'contacts_data': ('Контакты', 'contacts'),
            'hidden_menu': ('Скрытый элемент', 'hidden'),
        }

        cls.client = Client()
        cls.main = MenuItem.objects.create(
            name=cls.data['main_data'][0],
            menu_name=cls.menu_name,
            named_url=cls.data['main_data'][1],
        )
        cls.about = MenuItem.objects.create(
            name=cls.data['about_data'][0],
            menu_name=cls.menu_name,
            parent=cls.main,
            named_url=cls.data['about_data'][1],
        )
        cls.contacts = MenuItem.objects.create(
            name=cls.data['contacts_data'][0],
            menu_name=cls.menu_name,
            parent=cls.main,
            named_url=cls.data['contacts_data'][1],
        )
        cls.hidden = MenuItem.objects.create(
            name=cls.data['hidden_menu'][0],
            menu_name=cls.menu_name,
            parent=cls.contacts,
            named_url=cls.data['hidden_menu'][1],
        )

    def test_menu_on_page(self):
        """Тест отображения меню на странице"""
        response = self.client.get(reverse(self.data['main_data'][1]))
        self.assertContains(response, self.data['main_data'][0])
        self.assertContains(response, self.data['about_data'][0])
        self.assertContains(response, self.data['contacts_data'][0])
        self.assertNotContains(response, self.data['hidden_menu'][0])

    def test_db_menu(self):
        queryset = MenuItem.objects.all()
        # Проверка количества элементов в базе
        self.assertEqual(queryset.count(), len(self.data.items()))
        # Проверка главого меню
        self.assertEqual(queryset.get(name=self.data['main_data'][0]), self.main)
        # Проверка пункта about
        self.assertEqual(queryset.get(name=self.data['about_data'][0]), self.about)
        self.assertEqual(self.about.parent, self.main)
        # Проверка тестовой вкладки контакты
        self.assertEqual(queryset.get(name=self.data['contacts_data'][0]), self.contacts)
        self.assertEqual(self.contacts.parent, self.main)
        # Проверка скрытого меню
        self.assertEqual(queryset.get(name=self.data['hidden_menu'][0]), self.hidden)
        self.assertEqual(self.hidden.parent, self.contacts)