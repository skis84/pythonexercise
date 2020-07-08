from django.db import models

"""
.. module:: models
   :synopsis: Contains models for the company API
.. moduleauthor:: Sanna Luukkonen
"""


class Company(models.Model):
    business_id = models.SlugField(max_length=9, primary_key=True)
    # This field is added for convenience in admin panel,
    # the actual names are stored in Name table
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.business_id


class CompanyData(models.Model):
    # 1 for current version, >1 for historical data
    version = models.CharField(max_length=1, default='1')
    # 0 common, 1 = PRH, 2 = Verohallinto, 3 = BIS
    source = models.CharField(max_length=1, null=True)
    registration_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, blank=True, null=True)
    data_type = models.CharField(max_length=127)

    class Meta:
        abstract = True
        ordering = ('-modified',)


class Name(CompanyData):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class Address(CompanyData):
    street = models.CharField(max_length=255)
    post_code = models.SlugField(max_length=5)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.street + ", " + self.post_code + " " + self.city


class PhoneNumber(CompanyData):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class Website(CompanyData):
    value = models.URLField()

    def __str__(self):
        return self.value
