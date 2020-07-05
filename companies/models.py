from django.db import models

# Models for storing company information to database


class Company(models.Model):
    business_id = models.SlugField(max_length=9, primary_key=True)
    name = models.CharField(max_length=255, default='')


class TimeData(models.Model):
    registration_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField()

    class Meta:
        abstract = True


class Address(TimeData):
    street = models.CharField(max_length=255)
    post_code = models.SlugField(max_length=5)
    city = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class PhoneNumber(TimeData):
    value = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Website(TimeData):
    value = models.URLField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
