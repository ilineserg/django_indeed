from django.db import models


class Company(models.Model):

    uid = models.CharField(max_length=200, unique=True)

    name = models.TextField()
    link = models.TextField()
    about = models.TextField()

    headquarters = models.TextField()
    employees = models.TextField()
    industry = models.TextField()
    revenue = models.TextField()
    website = models.TextField()
