# -*- coding: utf-8 -*-
"""This migration shows a manual migration where a non-null field is added.
We can use code to add some wisdom
"""
from __future__ import unicode_literals
from django.db import migrations

import autoslug.fields


def populate_names(apps, schema_editor):
    """Fix new slug name
    """
    from autoslug.settings import slugify
    Contact = apps.get_model('notebook', 'Contact')
    for contact in Contact.objects.all():
        contact.slug = slugify("%s %s" % (contact.first_name,
                                          contact.last_name))
        contact.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='slug',
            field=autoslug.fields.AutoSlugField(
                verbose_name='Slug', null=True, editable=False),
            preserve_default=True,
        ),
        migrations.RunPython(populate_names),
        migrations.AlterField(
            model_name='contact',
            name='slug',
            field=autoslug.fields.AutoSlugField(verbose_name='Slug',
                                                unique=True, editable=False),
            preserve_default=True,
        ),

    ]
