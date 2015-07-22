from django.test import TestCase
from django.core.urlresolvers import reverse

class PollsTests(TestCase):

    def test_index_page(self):
        """Simple test for index page
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the polls index.")
