# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_questionnaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=500)),
                ('help_text', models.CharField(max_length=120)),
                ('error_text', models.CharField(max_length=120)),
                ('questionnaire', models.ForeignKey(to='survey.Questionnaire')),
            ],
        ),
    ]
