# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djanglavel.notebook.models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0002_manual_20150723_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='birthday',
            field=models.DateField(verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(verbose_name='Firstname', max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(verbose_name='Lastname', max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='slug',
            field=autoslug.fields.AutoSlugField(verbose_name='Slug', unique=True, editable=False, populate_from=djanglavel.notebook.models.Contact.get_full_name),
        ),
    ]
