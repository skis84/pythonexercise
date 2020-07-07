import requests
from .models import Address, Name, PhoneNumber, Website


class BusinessDataService:
    api_url = "https://avoindata.prh.fi/bis/v1/"
    reg_date_label = "registrationDate"
    end_date_label = "endDate"
    lang_label = "language"
    version_label = "version"
    source_label = "source"
    country_label = "country"
    address_type_label = "type"

    def __init__(self):
        self.jsonData = ""
        self.results = ""

    def get_results(self, company_id):
        response = requests.get(self.api_url + company_id)
        self.jsonData = response.json()
        self.results = self.jsonData["results"]
        return self.jsonData

    def save_data_to_db(self, array_label, type_label, accepted_data_types,
                        data_label, class_name, company,
                        get_data_from_db=None, create_db_object=None):

        if get_data_from_db is None:
            get_data_from_db = self.get_data_from_db

        if create_db_object is None:
            create_db_object = self.create_db_object

        for data in self.get_result()[array_label]:

            data_from_db = get_data_from_db(company, data, class_name,
                                            data_label, type_label)

            if self.is_valid(data):
                data_not_empty = data.get(data_label) != ""
                correct_data_type = data.get(type_label) in accepted_data_types
                not_in_db = data_from_db is None

                if data_not_empty and correct_data_type and not_in_db:
                    # Does not exist, create it
                    data = create_db_object(company, data,
                                            class_name, data_label,
                                            type_label)
                    data.save()
            elif data_from_db:
                # This piece of data is in the db but is not valid, so set
                # end date and version to correct values
                data_from_db.end_date = data.get(self.end_date_label)
                data_from_db.version = data.get(self.version_label)
                data_from_db.save()

    def get_business_id(self):
        return self.get_result()["businessId"]

    def number_of_results(self):
        return len(self.jsonData["results"])

    def get_result(self):
        return self.results[0]

    def get_address_from_db(self, company, addr_in_json, class_name=None,
                            data_label="", type_label=""):
        try:
            return Address.objects.filter(
                    street=addr_in_json.get("street"),
                    post_code=addr_in_json.get("postCode"),
                    city=addr_in_json.get("city"),
                    data_type=addr_in_json.get(self.address_type_label),
                    company=company,
                    language=addr_in_json.get(self.lang_label),
                    registration_date=addr_in_json.get(self.reg_date_label))[0]
        except IndexError:
            return None

    def create_address(self, company, address, class_name="",
                       data_label="", type_label=""):
        return Address(street=address.get("street"),
                       post_code=address.get("postCode"),
                       city=address.get("city"),
                       registration_date=address.get(self.reg_date_label),
                       end_date=None,
                       company=company,
                       language=address.get(self.lang_label),
                       data_type=address.get(self.address_type_label),
                       country=address.get(self.country_label),
                       source=address.get(self.source_label),
                       version=address.get(self.version_label)
                       )

    def get_data_from_db(self, company, data, class_name,
                         data_label, type_label):
        try:
            return class_name.objects.filter(
                    value=data.get(data_label),
                    data_type=data.get(type_label),
                    company=company,
                    language=data.get(self.lang_label),
                    registration_date=data.get(self.reg_date_label))[0]
        except IndexError:
            return None

    def is_valid(self, data):
        return data.get(self.end_date_label) is None

    def create_db_object(self, company, data,
                         class_name, data_label, type_label):
        return class_name(value=data.get(data_label),
                          registration_date=data.get(self.reg_date_label),
                          end_date=None,
                          company=company,
                          data_type=data.get(type_label),
                          language=data.get(self.lang_label),
                          source=data.get(self.source_label),
                          version=data.get(self.version_label))

    def form_response_from_db(self, business_id):
        name = Name.objects.filter(company=business_id)

        # Order by type so that possible street address comes before
        # postal address
        address_results = Address.objects.filter(
            company=business_id, end_date=None).order_by("data_type")

        address = (address_results[0].street + ", " +
                   address_results[0].post_code + " " +
                   address_results[0].city) if len(address_results) > 0 else ""

        phone_results = PhoneNumber.objects.filter(company=business_id,
                                                   end_date=None)
        phone = phone_results[0].value if len(phone_results) > 0 else ""

        website_results = Website.objects.filter(company=business_id,
                                                 end_date=None)
        website = website_results[0].value if len(website_results) > 0 else ""

        return {"business_id": business_id,
                "name": name[0].value,
                "address": address,
                "phone": phone,
                "website": website}
