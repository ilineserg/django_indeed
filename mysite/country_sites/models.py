from django.db import models


# Create your models here.
class IndeedCountrySites(models.Model):
    name = models.CharField(max_length=2048, null=True, blank=True)
    site = models.CharField(max_length=2048, null=True, blank=True)
    code_iso = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'coutry_sites'
