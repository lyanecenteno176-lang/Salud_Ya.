from django.test import TestCase
from django.urls import reverse

from saludya_app.models import MarketplaceCategory, Product


class IndexViewTests(TestCase):
    def test_home_page_uses_index_template(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saludya_app/Index.html')


class MarketplaceViewTests(TestCase):
    def test_marketplace_uses_market_template(self):
        response = self.client.get(reverse('marketplace'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saludya_app/market.html')
        self.assertContains(response, 'Marketplace SaludYa')
        self.assertContains(response, 'Alimentos Saludables')
        self.assertContains(response, 'market.js')
        self.assertContains(response, 'market.css')

    def test_marketplace_has_search_and_filters(self):
        response = self.client.get(reverse('marketplace'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'searchInput')
        self.assertContains(response, 'mainCategoryButtons')
        self.assertContains(response, 'subcategoryButtons')
