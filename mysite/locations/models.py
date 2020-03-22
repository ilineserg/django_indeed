from django.db import models


# Create your models here.
class Locations(models.Model):
    country = models.ForeignKey('country_sites.IndeedCountrySites', null=True,
                                blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=2048, null=True, blank=True)
    city = models.CharField(max_length=2048, null=True, blank=True)
    code_state = models.CharField(max_length=50, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'locations'