from django.db import models


class ApolloCompanyLinks(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'apollo_company_links'


class ApolloCompany(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    website = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    number_of_employees = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    tags = models.CharField(max_length=2048, null=True, blank=True)
    description_html = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    tech_used = models.ForeignKey('apollo.ApolloTechUsed', null=True,
                                  blank=True, on_delete=models.CASCADE)

    employees = models.ForeignKey('apollo.ApolloEmployees', null=True,
                                  blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'apollo_company'


class ApolloTechUsed(models.Model):
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=2048, null=True, blank=True)

    class Meta:
        db_table = 'apollo_tech_used'


class ApolloEmployees(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = 'apollo_employees'