# Generated by Django 3.0.3 on 2020-03-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indeedcountrysites',
            name='states_link',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterModelTable(
            name='indeedcountrysites',
            table='country_sites',
        ),
    ]
