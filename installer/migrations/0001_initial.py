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
        is_staff=True,
        first_name='Admin',
        last_name='User'
    )

    author = User.objects.create(
        username='user@ons.gov.uk',
        email='user@ons.gov.uk',
        password=make_password('password'),
        is_superuser=False,
        is_staff=True,
        first_name='Example',
        last_name='User'
    )
    

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
