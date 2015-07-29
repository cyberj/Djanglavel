from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Contact, Email
from datetime import date


class NotebookTests(TestCase):

    def test_index_page(self):
        """Simple test for index page using old style views
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

    def test_list_page(self):
        """Test Class-Based View list
        """
        c1 = Contact.objects.create(first_name="Dave", last_name="Null",
                                    birthday=date(2015, 1, 1))
        c2 = Contact.objects.create(first_name="Foo", last_name="Bar",
                                    birthday=date(2015, 1, 1))
        c3 = Contact.objects.create(first_name="Hello", last_name="World",
                                    birthday=date(2015, 1, 1))
        response = self.client.get(reverse('notebook:list'))
        # Check for names
        self.assertContains(response, c1.get_full_name())
        self.assertContains(response, c2.get_full_name())
        self.assertContains(response, c3.get_full_name())
        # Check for detail link
        self.assertContains(response, reverse('notebook:detail', args=[c1.slug]))
        self.assertContains(response, reverse('notebook:detail', args=[c2.slug]))
        self.assertContains(response, reverse('notebook:detail', args=[c3.slug]))

    def test_detail_page(self):
        """Test Class-Based View Detail
        """
        # Try with empty data
        response = self.client.get(reverse('notebook:detail',
                                           kwargs={'slug': "dave-null"}))
        self.assertEqual(response.status_code, 404)
        # Create Dave
        c1 = Contact.objects.create(first_name="Dave", last_name="Null",
                                    birthday=date(2015, 1, 1))
        c1_e1 = Email.objects.create(contact=c1, email="davenull@42.com")
        c1_e2 = Email.objects.create(contact=c1, email="daverandom@42.com")
        # Get details
        response = self.client.get(reverse('notebook:detail',
                                           kwargs={'slug': "dave-null"}))
        self.assertContains(response, c1.first_name)
        self.assertContains(response, c1.last_name)
        self.assertContains(response, "01/01/2015")
        self.assertContains(response, c1_e1.email)
        self.assertContains(response, c1_e2.email)

    def test_create_form(self):
        """Test Class-based View Create
        """
        # Spawn create view
        response = self.client.get(reverse('notebook:create'))
        self.assertEqual(response.status_code, 200)
        payload = {
            'first_name': "Dave",
            'last_name': "Null",
            'birthday': "2015-01-01"
        }
        # Post in create view
        response = self.client.post(reverse('notebook:create'), payload)
        # All good, redirecting
        self.assertRedirects(response, reverse('notebook:detail', args=['dave-null']))
        # Should get it in DB
        cc = Contact.objects.get(slug="dave-null")
        self.assertEquals(cc.birthday, date(2015, 1, 1))

    def test_update_form(self):
        """Test Class-based View Update
        """
        # Create and get form
        c1 = Contact.objects.create(first_name="Dave", last_name="Null",
                                    birthday=date(2015, 1, 1))
        dave_update_url = reverse("notebook:update", kwargs={"slug": c1.slug})
        response = self.client.get(dave_update_url)
        self.assertEqual(response.status_code, 200)
        # Modify form
        payload = {
            'first_name': "Dave",
            'last_name': "Random",
            'birthday': "2015-02-02"
        }
        response = self.client.post(dave_update_url, payload)
        # Profit
        c1 = Contact.objects.get(id=c1.id)
        self.assertRedirects(response, reverse('notebook:detail', args=['dave-null']))
        self.assertEqual(c1.birthday, date(2015, 2, 2))
        self.assertEqual(c1.last_name, "Random")
