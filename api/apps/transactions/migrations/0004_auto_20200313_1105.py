# Generated by Django 2.1 on 2020-03-13 11:05

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0003_auto_20200130_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateField(auto_now_add=True,
                                   default=datetime.datetime(2020, 3, 13, 11, 5, 33, 719445, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
