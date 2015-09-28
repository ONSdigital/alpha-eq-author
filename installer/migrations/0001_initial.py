# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_registered_model('auth', 'User')
    superuser = User.objects.create(
        username='admin',
        email='admin@example.com',
        password=make_password('password'),
        is_superuser=True,
        is_staff=True
    )

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
