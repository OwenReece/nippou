# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nippou_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nippou',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
