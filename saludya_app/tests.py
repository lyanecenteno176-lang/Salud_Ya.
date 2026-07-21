from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_home_page_uses_index_template(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saludya_app/Index.html')
