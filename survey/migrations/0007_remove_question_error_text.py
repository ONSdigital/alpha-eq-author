# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_questionnaire_introduction_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='error_text',
        ),
    ]
