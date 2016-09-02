# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readonly_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            ['''ALTER TABLE readonly_app_car ALTER COLUMN manufacturer SET DEFAULT 'Renault';'''])
    ]
