# Generated by Django 2.1 on 2020-03-13 11:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('wallet', '0002_auto_20200126_2244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='bal',
            new_name='balance',
        ),
    ]
