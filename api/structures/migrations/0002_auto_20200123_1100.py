# Generated by Django 2.1 on 2020-01-23 11:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]