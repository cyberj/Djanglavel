from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question

class PollsTests(TestCase):

    def test_index_page(self):
        """Simple test for index page
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        question_text = "Thats is the question"
        self.assertNotContains(response, question_text)
        Question.objects.create(question_text=question_text)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, question_text)
