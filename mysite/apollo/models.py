from django.db import models


# Create your models here.
class AppoloCompanyLinks(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'apollo_company_links'