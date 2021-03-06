# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='questionnaire_id',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
