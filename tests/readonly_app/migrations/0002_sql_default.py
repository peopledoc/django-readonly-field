# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readonly_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL([
            '''ALTER TABLE readonly_app_car '''
            '''ALTER COLUMN manufacturer SET DEFAULT 'Renault';''',

            '''ALTER TABLE readonly_app_bus '''
            '''ALTER COLUMN wheel_number SET DEFAULT 22;'''

            '''ALTER TABLE readonly_app_book '''
            '''ALTER COLUMN iban SET DEFAULT '1234-abcd';''',

            '''ALTER TABLE readonly_app_book '''
            '''ALTER COLUMN ref SET DEFAULT 123456789;'''])
    ]
