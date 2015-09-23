# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionnaire_id', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=120)),
                ('overview', models.TextField(max_length=3000)),
                ('survey', models.ForeignKey(to='survey.Survey')),
            ],
        ),
    ]
