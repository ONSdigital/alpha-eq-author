# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_questionnaire_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='introduction_text',
            field=models.TextField(default='', max_length=3000),
            preserve_default=False,
        ),
    ]
