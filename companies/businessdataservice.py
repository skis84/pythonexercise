import requests
from .models import Address, Name, PhoneNumber, Website


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

    def number_of_results(self):
        return len(self.jsonData["results"])

    def get_result(self):
        return self.results[0]

    def save_addresses_to_db(self, company):
        street = ""
        postcode = ""
        city = ""
        addresses = self.get_result()["addresses"]
        for address in addresses:
            if self.is_valid(address) and address["street"] != "":
                street = address.get("street")
                postcode = address.get("postCode")
                city = address.get("city")
                country = address.get("country")
                registration_date = address.get("registrationDate")
                address_type = address.get("type")
                language = address.get("language")

                # Check if address already exists in db
                result = Address.objects.filter(
                    street=street,
                    company=company.business_id,
                    registration_date=registration_date)

                result_length = len(result)

                if result_length == 0:
                    # Does not exist, create it
                    address = Address(street=street,
                                      post_code=postcode,
                                      city=city,
                                      country=country,
                                      type=address_type,
                                      registration_date=registration_date,
                                      end_date=None,
                                      language=language,
                                      company=company
                                      )
                    address.save()
                elif result_length == 1:
                    # Check if data needs to be updated
                    address_in_db = result[0]
                    if address_in_db.needs_update(street, postcode, city):
                        address_in_db.street = street
                        address_in_db.postcode = postcode
                        address_in_db.city = city
                        address_in_db.save()
            else:
                # TODO Check if valid address has ended
                # return f"{street} {postcode} {city}"
                # return ""
                pass

    def is_valid(self, data):
        return data["endDate"] is None

    def save_data_to_db(self, arrayLabel, dataTypes, dataLabel,
                        className, company):
        dataArray = self.get_result()[arrayLabel]
        for data in dataArray:
            if(self.is_valid(data)):

                if "type" in data and data["type"] in dataTypes:
                    value = data[dataLabel]
                    registration_date = data["registrationDate"]

                    # Check if data already exists in db
                    data_from_db = className.objects.filter(
                        value=value,
                        company=company.business_id,
                        registration_date=registration_date)

                    result_length = len(data_from_db)

                    if result_length == 0:
                        # Does not exist, create it
                        data = className(value=value,
                                         registration_date=registration_date,
                                         end_date=None,
                                         company=company)
                        data.save()
                    elif result_length == 1:
                        # Check if data needs to be updated
                        data = data_from_db[0]
                        if data.value != value:
                            data.value = value
                            data.save()

    def form_response_from_db(self, business_id):
        name = Name.objects.filter(company=business_id)

        address_results = Address.objects.filter(
            company=business_id).exclude(street__startswith="PL")
        address = (address_results[0].street + ", " +
                   address_results[0].post_code + " " +
                   address_results[0].city) if len(address_results) > 0 else ""

        phone_results = PhoneNumber.objects.filter(company=business_id)
        phone = phone_results[0].value if len(phone_results) > 0 else ""

        website_results = Website.objects.filter(company=business_id)
        website = website_results[0].value if len(website_results) > 0 else ""

        return {"business_id": business_id,
                "name": name[0].value,
                "address": address,
                "phone": phone,
                "website": website}
