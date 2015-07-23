from django.db import models


class Contact(models.Model):
    """Contact in a Notebook"""
    first_name = models.CharField('Firstname', max_length=200)
    last_name = models.CharField('Lastname', max_length=200)
    birthday = models.DateTimeField('Birthday')


class Email(models.Model):
    """Email for a Contact"""
    contact = models.ForeignKey(Contact)
    email = models.EmailField()
