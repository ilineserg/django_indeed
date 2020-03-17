from django.contrib.postgres.fields import JSONField
from django.db import models


class CompanyLusha(models.Model):
    title = models.CharField(max_length=500)
    # ^ class company-info -> class text-block -> h1
    link = models.CharField(max_length=2048, null=True, blank=True)
    # ^
    link_outer = models.CharField(max_length=2048, null=True, blank=True)
    # ^ class company-info -> class text-block -> class link -> h2 -> a
    description_text = models.TextField(null=True, blank=True)
    # ^ class company-info -> class text-block -> p
    description_html = models.TextField(null=True, blank=True)
    # ^ class company-info
    company_details = JSONField(default=str)
    # ^ dl class company-details
    company_social_networks = JSONField(default=str)
    # ^ ul class company-social-networks
    email_address_formats = JSONField(default=str)
    # ^ class formats-table -> table -> (for tr) -> key: td[1], value: td[2]

    class Meta:
        db_table = 'companies_lusha'
