# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_lock_questionnaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='last_used_id',
            field=models.IntegerField(default=0),
        ),
    ]
