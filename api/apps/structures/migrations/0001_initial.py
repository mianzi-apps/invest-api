# Generated by Django 2.1 on 2020-01-23 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('farms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=255)),
                ('purpose', models.TextField(max_length=300)),
                ('capacity', models.IntegerField()),
                ('dimensions', models.CharField(max_length=150)),
                ('setup_cost', models.IntegerField()),
                ('farm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farms.Farm')),
            ],
        ),
    ]
