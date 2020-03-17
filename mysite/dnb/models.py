from django.contrib.postgres.fields import JSONField
from django.db import models


class CompanyDNB(models.Model):
    link = models.CharField(max_length=2500, null=True, blank=True, unique=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    # ^ <h1 class="title">TOYOTA MOTOR CORPORATION</h1>
    address = models.CharField(max_length=2048, null=True, blank=True)
    address_html = models.CharField(max_length=2048, null=True, blank=True)
    # ^ <div class="address">
    phone = models.CharField(max_length=2048, null=True, blank=True)

    website = models.CharField(max_length=2048, null=True, blank=True)
    # ^ <div class='web'><a href="http://www.toyota.co.jp" target="_blank" rel="nofollow" id="hero-company-link">www.toyota.co.jp</a>
    #   </div>
    company_type = models.CharField(max_length=2048, null=True, blank=True)
    company_role = models.CharField(max_length=2048, null=True, blank=True)
    # ^ <span class="type-role-label">
    #                                     Company Type:</span>
    #                                 <span class="type">Corporation</span>
    #                                 <span class="role">Parent</span>
    #                                 </div>
    description_text = models.TextField(null=True, blank=True)
    # <span class="company_summary"><p><span class="strength">Toyota Motor is among the world's largest automotive manufacturers. The company designs and manufactures a diverse product line-up that ranges from subcompacts to luxury and sports vehicles to SUVs, trucks, minivans, and buses.</span> Its vehicles are produced either with combustion engines or hybrid-electric propulsion systems, as with the iconic Prius. Popular models include the Camry, Corolla, Land Cruiser, and luxury Lexus line, as well as the Tundra truck. Toyota's subsidiaries also manufacture vehicles: Daihatsu Motor produces mini-vehicles, while Hino Motors produces trucks and buses. Additionally, Toyota makes automotive parts for its own use and for sale to others. The company's domestic sales account for approximately 45% of the company's revenue.</p><dnb:rewrite><a href="/products/marketing-sales/dnb-hoovers/free-trial.html">Try D&B Hoovers Free</a></dnb:rewrite></span>
    employees = models.CharField(max_length=500, null=True, blank=True)
    # <li class="empCon">
    #                     <span class="key">&nbsp;EMPLOYEES (All Sites)</span>
    #                     <span class="value ">370,870</span>
    incorporated = models.CharField(max_length=500, null=True, blank=True)
    # <li class="founded">
    #                     <span class="key">Incorporated</span>
    #                     <span class="value ">1937</span>
    corporate_family_connections = models.CharField(max_length=500, null=True, blank=True)
    # <div class="count">

    class Meta:
        db_table = 'companies_dnb'


class IndusryDNB(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'industries_dnb'


class CountryIndusryDNB(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    country = models.CharField(max_length=500)

    class Meta:
        db_table = 'country_industries_dnb'


class ShortCountryDNB(models.Model):
    title = models.CharField(max_length=2500)
    link = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    country = models.CharField(max_length=2500)

    class Meta:
        db_table = 'short_country_dnb'



