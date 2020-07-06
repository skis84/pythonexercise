from django.db import models

# Models for storing company information to database


class Company(models.Model):
    business_id = models.SlugField(max_length=9, primary_key=True)


class CompanyData(models.Model):
    registration_date = models.DateField()
    end_date = models.DateField(null=True)
    modified = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Name(CompanyData):
    value = models.CharField(max_length=255)


class Address(CompanyData):
    street = models.CharField(max_length=255)
    post_code = models.SlugField(max_length=5)
    city = models.CharField(max_length=255)

    def needs_update(self, street, postcode, city):
        if(self.street != street):
            return True
        elif(self.post_code != postcode):
            return True
        elif(self.city != city):
            return True
        else:
            return False


class PhoneNumber(CompanyData):
    value = models.CharField(max_length=255)


class Website(CompanyData):
    value = models.URLField()
