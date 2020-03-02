from django.contrib.postgres.fields import JSONField
from django.db import models


class Vacancy(models.Model):
    company = models.ForeignKey('companies.Company', null=True, blank=True)

    job_key = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True)
    description_text = models.TextField(null=True, blank=True)
    description_html = models.TextField(null=True, blank=True)

    location = models.CharField(max_length=500, null=True, blank=True)
    location_uid = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)

    company_name = models.CharField(max_length=500, null=True, blank=True)
    company_link = models.CharField(max_length=2048, null=True, blank=True)
    company_uid = models.CharField(max_length=200, null=True, blank=True)

    raw_data = JSONField(default='')

    class Meta:
        db_table = 'vacancies'
