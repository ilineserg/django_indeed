from django.contrib.postgres.fields import JSONField
from django.db import models


class Vacancies(models.Model):
    company_id = models.ForeignKey('companies.Company', nullable=True)

    job_key = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, nullable=True)
    description_text = models.TextField
    description_html = models.TextField

    location = models.CharField(max_length=500, nullable=True)
    location_uid = models.CharField(max_length=200, nullable=True)
    country = models.CharField(max_length=500, nullable=True)
    zip = models.CharField(max_length=50, nullable=True)
    city = models.CharField(max_length=500, nullable=True)

    company_name = models.CharField(max_length=500, nullable=True)
    company_link = models.CharField(max_length=2048, nullable=True)
    company_uid = models.CharField(max_length=200, nullable=True)

    raw_data = JSONField(default='')
