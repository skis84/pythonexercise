from django.db import models

"""
   :synopsis: Contains models for the company API
.. moduleauthor:: Sanna Luukkonen
"""


class Company(models.Model):
    '''Model class for company'''
    business_id = models.SlugField(max_length=9, primary_key=True)
    # This field is added for convenience in admin panel,
    # the actual names are stored in Name table
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.business_id


class CompanyData(models.Model):
    '''Base class for company data'''
    # 1 for current version, >1 for historical data
    version = models.CharField(max_length=1, default='1')
    # 0 common, 1 = PRH, 2 = Verohallinto, 3 = BIS
    source = models.CharField(max_length=1, null=True)
    # This should not optional according to the specification of BIS opendata,
    # but there is data that does not have this field set
    registration_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, blank=True, null=True)
    data_type = models.CharField(max_length=127)

    class Meta:
        abstract = True
        ordering = ('-modified',)


class Name(CompanyData):
    '''Name class for storing company names'''
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class Address(CompanyData):
    '''Address class for storing company addresses'''
    street = models.CharField(max_length=255)
    post_code = models.SlugField(max_length=5)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.street + ", " + self.post_code + " " + self.city


class PhoneNumber(CompanyData):
    '''PhoneNumber class for storing company phone numbers'''
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class Website(CompanyData):
    '''Website class for storing company websites'''
    value = models.URLField()

    def __str__(self):
        return self.value
