# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_registered_model('auth', 'User')
    superuser = User.objects.create(
        username='admin',
        email='admin@example.com',
        password="pbkdf2_sha256$20000$njbkVZfblckF$AaE20dfQWsS0OHVan88+rf5/Mt2+1BiIYzY5fU6Uqqg=",
        is_superuser=True,
        is_staff=True,
        first_name='Admin',
        last_name='User'
    )

    user1 = User.objects.create(
        username='han',
        email='hansolo@example.com',
        password="pbkdf2_sha256$20000$eIIcKQ10Rsp1$xwT3oP7Szq6imOJ9l19M+7Rf5VzPiIUxhQtHgoYXMT0=",
        is_superuser=False,
        is_staff=True,
        first_name='Han',
        last_name='Solo'
    )

    user2 = User.objects.create(
        username='luke',
        email='lukeskywalker@example.com',
        password="pbkdf2_sha256$20000$mh5U3dnDMl1L$mj+Z+VdH/Kt6BIJ/EtU+UK1YG0cN4sDi/+ll1gSHGSs=",
        is_superuser=False,
        is_staff=True,
        first_name='Luke',
        last_name='Skywalker'
    )

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
