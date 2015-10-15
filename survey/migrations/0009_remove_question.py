# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_add_questionnaire_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='questionnaire',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
