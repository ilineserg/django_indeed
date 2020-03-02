from django.db import models


class Company(models.Model):

    uid = models.CharField(max_length=200, unique=True)

    name = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=2048, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    headquarters = models.TextField(null=True, blank=True)
    employees = models.TextField(null=True, blank=True)
    industry = models.TextField(null=True, blank=True)
    revenue = models.TextField(null=True, blank=True)
    website = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'companies'