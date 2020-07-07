from django.db import models

# Models for storing company information to database


class Company(models.Model):
    business_id = models.SlugField(max_length=9, primary_key=True)


class CompanyData(models.Model):
    # 1 for current version, >1 for historical data
    version = models.CharField(max_length=1, default='1')
    # 0 common, 1 = PRH, 2 = Verohallinto, 3 = BIS
    source = models.CharField(max_length=1, null=True)
    registration_date = models.DateField()
    end_date = models.DateField(null=True)
    modified = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, null=True)
    data_type = models.CharField(max_length=127)

    class Meta:
        abstract = True


class Name(CompanyData):
    value = models.CharField(max_length=255)


class Address(CompanyData):
    street = models.CharField(max_length=255)
    post_code = models.SlugField(max_length=5)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=2, null=True)


class PhoneNumber(CompanyData):
    value = models.CharField(max_length=255)


class Website(CompanyData):
    value = models.URLField()
