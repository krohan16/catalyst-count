# Generated by Django 5.1.3 on 2024-11-26 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='year_founded',
            field=models.IntegerField(null=True),
        ),
    ]
