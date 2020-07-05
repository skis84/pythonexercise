import requests
from .models import Address
from datetime import datetime


class BusinessDataService:
    api_url = "https://avoindata.prh.fi/bis/v1/"

    def __init__(self):
        self.jsonData = ""
        self.results = ""

    def get_results(self, company_id):
        response = requests.get(self.api_url + company_id)
        self.jsonData = response.json()
        self.results = self.jsonData["results"]
        return self.jsonData

    def get_business_id(self):
        return self.results[0]["businessId"]

    def get_name(self):
        return self.results[0]["name"]

    def number_of_results(self):
        return len(self.jsonData["results"])

    def get_result(self):
        return self.results[0]

    def getAddressAndSaveToDb(self, company):
        street = ""
        postcode = ""
        city = ""
        addresses = self.get_result()["addresses"]
        for address in addresses:
            if self.isValid(address) and address["street"] != "":
                street = address["street"]
                postcode = address["postCode"]
                city = address["city"]
                registration_date = address["registrationDate"]

                # Check if address already exists in db
                result = Address.objects.filter(
                    company=company.business_id,
                    registration_date=registration_date)

                result_length = len(result)

                if result_length == 0:
                    # Does not exist, create it
                    address = Address(street=street,
                                      post_code=postcode,
                                      city=city,
                                      registration_date=registration_date,
                                      end_date=None,
                                      modified_date=datetime.now(),
                                      company=company
                                      )
                    address.save()
                elif result_length == 1:
                    # TODO Check if data needs to be updated
                    address_in_db = result[0]
                    print(address_in_db.street,
                          address_in_db.post_code, address_in_db.city)

                return f"{street} {postcode} {city}"
        return ""

    def isValid(self, data):
        return data["endDate"] is None

    def getDetailAndSaveToDb(self, contactDetailLabel,
                             className,
                             company):
        contactDetails = self.get_result()["contactDetails"]
        for contact in contactDetails:
            if(self.isValid(contact)):

                if contact["type"] == contactDetailLabel:
                    value = contact["value"]
                    registration_date = contact["registrationDate"]

                    # Check if contact detail already exists in db
                    contact_from_db = className.objects.filter(
                        company=company.business_id,
                        registration_date=registration_date)

                    result_length = len(contact_from_db)

                    if result_length == 0:
                        # Does not exist, create it
                        detail = className(value=value,
                                           registration_date=registration_date,
                                           end_date=None,
                                           modified_date=datetime.now(),
                                           company=company)
                        detail.save()
                    elif result_length == 1:
                        # Check if data needs to be updated
                        contact = contact_from_db[0]
                        if contact.value != value:
                            contact.value = value
                            contact.save()
                            print("Value saved to DB")
                        else:
                            print("Value not saved")
                    return value
        return ""
