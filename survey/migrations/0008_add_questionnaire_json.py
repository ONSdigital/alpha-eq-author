# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_remove_question_error_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.TextField(default='DefaultQuestion', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='questionnaire_json',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
    ]
