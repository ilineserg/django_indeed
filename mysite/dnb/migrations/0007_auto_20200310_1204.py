# Generated by Django 3.0.3 on 2020-03-10 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnb', '0006_auto_20200310_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydnb',
            name='link',
            field=models.CharField(blank=True, max_length=2500, null=True, unique=True),
        ),
    ]
