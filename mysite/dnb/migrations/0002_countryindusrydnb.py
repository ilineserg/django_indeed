# Generated by Django 3.0.3 on 2020-03-10 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryIndusryDNB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('link', models.CharField(blank=True, max_length=2048, null=True, unique=True)),
                ('country', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'country_industries_dnb',
            },
        ),
    ]
