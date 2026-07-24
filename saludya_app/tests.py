from django.test import TestCase
from django.urls import reverse

from saludya_app.models import MarketplaceCategory, Product


class IndexViewTests(TestCase):
    def test_home_page_uses_index_template(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saludya_app/Index.html')


class MarketplaceViewTests(TestCase):
    def setUp(self):
        food_category = MarketplaceCategory.objects.create(
            name='Alimentos Saludables',
            slug='alimentos-saludables',
            description='Productos alimenticios saludables',
        )
        Product.objects.create(
            category=food_category,
            name='Tazón energético de avena integral',
            description='Desayuno saludable con avena, frutos rojos y semillas.',
            price=120.00,
            image_url='/static/saludya_app/images/Avena-Integral.jpg',
            stock=50,
            featured=True,
        )
        Product.objects.create(
            category=food_category,
            name='Smoothie verde detox',
            description='Bebida natural de espinaca, manzana, plátano y jengibre.',
            price=85.00,
            image_url='/static/saludya_app/images/Espinaca.jpg',
            stock=40,
            featured=True,
        )

    def test_marketplace_renders_catalog_products(self):
        response = self.client.get(reverse('marketplace'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marketplace SaludYa')
        self.assertContains(response, 'Tazón energético de avena integral')
        self.assertContains(response, 'Smoothie verde detox')

    def test_marketplace_uses_local_static_images(self):
        response = self.client.get(reverse('marketplace'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'via.placeholder.com')
        self.assertContains(response, '/static/saludya_app/images/Avena-Integral.jpg')
        self.assertContains(response, '/static/saludya_app/images/Espinaca.jpg')
