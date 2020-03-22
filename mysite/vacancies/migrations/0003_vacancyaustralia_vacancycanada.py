# Generated by Django 3.0.3 on 2020-03-21 20:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_companyaustralia_companycanada'),
        ('vacancies', '0002_auto_20200302_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='VacancyCanada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_key', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('link', models.CharField(blank=True, max_length=2048, null=True)),
                ('description_text', models.TextField(blank=True, null=True)),
                ('description_html', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('location_uid', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('zip', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('company_name', models.CharField(blank=True, max_length=500, null=True)),
                ('company_link', models.CharField(blank=True, max_length=2048, null=True)),
                ('company_uid', models.CharField(blank=True, max_length=200, null=True)),
                ('raw_data', django.contrib.postgres.fields.jsonb.JSONField(default=str)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyCanada')),
            ],
            options={
                'db_table': 'vacancies_canada',
            },
        ),
        migrations.CreateModel(
            name='VacancyAustralia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_key', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('link', models.CharField(blank=True, max_length=2048, null=True)),
                ('description_text', models.TextField(blank=True, null=True)),
                ('description_html', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('location_uid', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('zip', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('company_name', models.CharField(blank=True, max_length=500, null=True)),
                ('company_link', models.CharField(blank=True, max_length=2048, null=True)),
                ('company_uid', models.CharField(blank=True, max_length=200, null=True)),
                ('raw_data', django.contrib.postgres.fields.jsonb.JSONField(default=str)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyAustralia')),
            ],
            options={
                'db_table': 'vacancies_australia',
            },
        ),
    ]
