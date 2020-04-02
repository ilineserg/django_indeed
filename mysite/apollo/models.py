from django.db import models
from django.contrib.postgres.fields import JSONField


class ApolloCompanyLinks(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'apollo_company_links'


class ApolloTags(models.Model):
    title = models.CharField(max_length=2048)

    class Meta:
        db_table = 'apollo_tags'


class ApolloCompany(models.Model):
    company_id_apollo = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    website = models.CharField(max_length=2048, null=True, blank=True,
                               unique=True)
    number_of_employees = models.CharField(max_length=500, null=True,
                                           blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    address = JSONField()
    tags = models.ManyToManyField(ApolloTags)
    description = models.TextField(null=True, blank=True)
    social_links = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'apollo_company'


class ApolloTechUsed(models.Model):
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=2048, null=True, blank=True)
    company = models.ForeignKey('apollo.ApolloCompany', null=True,
                                blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'apollo_tech_used'


class ApolloEmployees(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    position = models.CharField(max_length=1024, null=True, blank=True)
    company = models.ForeignKey('apollo.ApolloCompany', null=True,
                                blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'apollo_employees'
