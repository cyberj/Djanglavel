from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Contact
from datetime import date


class NotebookTests(TestCase):

    def test_index_page(self):
        """Simple test for index page
        """
        first_name = "Dave"
        last_name = "Null"
        birthday = date(2015, 1, 1)
        # No question : nothing to see
        response = self.client.get(reverse('notebook:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, first_name)
        # Question here : check it
        Contact.objects.create(first_name=first_name,
                               last_name=last_name, birthday=birthday)
        response = self.client.get(reverse('notebook:index'))
        self.assertContains(response, first_name)
        self.assertContains(response, last_name)
        self.assertContains(response, "01/01/2015")
#
#     def test_detail_page(self):
#         """Simple test for detail page
#         """
#         question_text = "Thats is the question"
#         # No question : get a 404
#         response = self.client.get(reverse('polls:detail', kwargs={"question_id": 1}))
#         self.assertEqual(response.status_code, 404)
#         # Question : Create it
#         q = Question.objects.create(question_text=question_text)
#         c1 = q.choice_set.create(choice_text="Yay")
#         c2 = q.choice_set.create(choice_text="Nay")
#         c3 = q.choice_set.create(choice_text="Eww")
#         # Check the choices
#         response = self.client.get(reverse('polls:detail', kwargs={"question_id": q.id}))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, q.question_text)
#         self.assertContains(response, c1.choice_text)
#         self.assertContains(response, c2.choice_text)
#         self.assertContains(response, c3.choice_text)
