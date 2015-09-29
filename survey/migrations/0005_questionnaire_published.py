# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_questionnaire_reviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
