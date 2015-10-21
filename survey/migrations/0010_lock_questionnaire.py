# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_remove_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='locked_by',
            field=models.TextField(default=None, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='locked_on',
            field=models.DateField(default=None, null=True),
        ),
    ]
