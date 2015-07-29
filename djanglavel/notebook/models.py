from django.db import models
from autoslug import AutoSlugField


class Contact(models.Model):

    """Contact in a Notebook"""
    first_name = models.CharField('Firstname', max_length=200)
    last_name = models.CharField('Lastname', max_length=200)
    birthday = models.DateField('Birthday')

    # Example of third party module : use a slug instead of id for URLs
    def get_full_name(self):
        """get full name for display or slugify"""
        return "%s %s" % (self.first_name, self.last_name)

    slug = AutoSlugField('Slug', unique=True, populate_from=get_full_name)

    def get_absolute_url(self):
        # Must import here to avoid circular imports
        from django.core.urlresolvers import reverse
        return reverse('notebook:detail', args=[self.slug])


class Email(models.Model):

    """Email for a Contact"""
    contact = models.ForeignKey(Contact)
    email = models.EmailField()
