from django.db import models
from autoslug import AutoSlugField


class Contact(models.Model):
    """Contact in a Notebook"""
    first_name = models.CharField('Firstname', max_length=200)
    last_name = models.CharField('Lastname', max_length=200)
    birthday = models.DateTimeField('Birthday')

    # Example of third party module : use a slug instead of id for URLs
    slug = AutoSlugField('Slug', unique=True, populate_from=lambda x: x.get_full_name())

    def get_full_name(self):
        """get full name for display or slugify"""
        return "%s %s" % (self.first_name, self.last_name)


class Email(models.Model):
    """Email for a Contact"""
    contact = models.ForeignKey(Contact)
    email = models.EmailField()
