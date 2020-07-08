import requests
from .models import Company, Address, Name, PhoneNumber, Website


class BusinessDataService:
    """ Class for fetching data from api endpoint and storing it to local db.
    """

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
        """ Gets results from the api endpoint and stores
        the result JSON in class property
        """
        response = requests.get(self.api_url + company_id)
        self.jsonData = response.json()
        self.results = self.jsonData["results"]
        return self.jsonData

    # Get company from db or create a new one
    # if company does not exist
    def get_company_from_db(self, business_id):
        ''' get company from db. Creates a new company if a
            company with the given business id is does not exist.

        :param business_id: Business id of the company to search for

        '''
        # Check if Company already exists in local db
        try:
            company = Company.objects.get(business_id=business_id)
        except Company.DoesNotExist:
            # If not, store it
            company = Company(business_id=business_id,
                              business_name=self.get_name())
            company.save()
        return company

    def save_data_to_db(self, array_label, type_label, accepted_data_types,
                        data_label, class_name, company,
                        get_data_from_db=None, create_db_object=None):
        '''Examines a certain subset of JSON result and stores data to db (SQLite3)

        :param array_label: The name of the subset in JSON to examine
                            e.g. "names"
        :param type_label: Label for the accepted type, e.g. order
        :param accepted_data_types_label: List of accepted data types, e.g. [0]
        :param data_label: Label of the data that should be selected,
                           e.g. "name"
        :param class_name: Class name of the model for the data in db
        :param company: Company object that data is related to
        :param get_data_from_db: Function for getting data from db to
                                 see if data already exists in db. If this
                                 parameter is omitted,
                                 the data model needs to be a subclass of
                                 CompanyData with an additional property called
                                 "value".
        :param create_db_object: Function for creating a new data model
                                 object. If this parameter is omitted,
                                 the data model needs to
                                 be a subclass of CompanyData with
                                 an additional property called "value".
        '''

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
        ''' Returns the business id if get_results has been called and
        business id was found from JSON data'''
        return self.get_result().get("businessId")

    def get_name(self):
        ''' Returns the company name if get_results has been called and
        business name was found from JSON data'''
        return self.get_result().get("name")

    def number_of_results(self):
        ''' Returns the number of results if get_results has been called and
        there are results'''
        return len(self.jsonData["results"])

    def get_result(self):
        ''' Returns the result array that contains the name, address and other
        relevant data'''
        return self.results[0]

    def get_address_from_db(self, company, addr_in_json, class_name=None,
                            data_label="", type_label=""):
        ''' Returns an Address object from the database.
        :params company: Company to which the address is related to
        :params addr_in_json: dictionary that contains the address data to
        search for
        :params class_name:
        :params data_label:
        :params type_label:

        '''
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
        ''' Returns a data model object from the database.
        :params company: Company to which the data is related to
        :params addr_in_json: dictionary that contains the data to
        search for
        :params class_name: The name of the model class to use in search
        :params data_label: The label for the data in the dictionary
        :params type_label: The label for the data type in the dictionary

        '''
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
        ''' Returns true if the data has no end date.'''
        return data.get(self.end_date_label) is None

    def create_db_object(self, company, data,
                         class_name, data_label, type_label):
        ''' Creates a new model object.

        :params company: Company to which the data is related to. This is used
                         as the foreign key for the data.
        :params data: dictionary that contains the new data
        :params class_name: The name of the model class to instantiate
        :params data_label: The label for the data in the dictionary
        :params type_label: The label for the data type in the dictionary'''
        return class_name(value=data.get(data_label),
                          registration_date=data.get(self.reg_date_label),
                          end_date=None,
                          company=company,
                          data_type=data.get(type_label),
                          language=data.get(self.lang_label),
                          source=data.get(self.source_label),
                          version=data.get(self.version_label))

    def form_response_from_db(self, business_id):
        ''' Returns a data model object from the database.

        : params company: Company to which the data is related to
        : params addr_in_json: dictionary that contains the data to
        search for
        : params class_name: The name of the model class to use in search
        : params data_label: The label for the data in the dictionary
        : params type_label: The label for the data type in the dictionary

        '''
        name = Name.objects.filter(company=business_id)

        # Order by type so that possible street address comes before
        # postal address
        address_results = Address.objects.filter(
            company=business_id, end_date=None).order_by("data_type").order_by(
                "-modified")

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
