# Generated by Django 2.1 on 2020-01-23 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255, null=True)),
                ('longitude', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='farm',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farms.Location'),
        ),
    ]