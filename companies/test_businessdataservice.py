from django.test import TestCase

from companies.businessdataservice import BusinessDataService
import json
from .models import Company, Name, Address, PhoneNumber, Website


class BusinessDataServiceTestCase(TestCase):

    def test_get_business_id(self):
        mock_service = MockBusinessDataService()
        self.assertEqual(mock_service.get_business_id(), "1234567-8")

    def test_save_data_to_db(self):
        mock_service = MockBusinessDataService()
        company = Company("1234567-8")
        company.save()
        mock_service.save_data_to_db("names", "order", [0], "name", Name,
                                     company)

        # Now database should have one name stored
        result = Name.objects.all()
        self.assertEqual(1, len(result))
        self.assertEqual("Nokia Oyj", result[0].value)

    def test_save_data_to_db_with_invalid_result_label(self):
        mock_service = MockBusinessDataService()
        company = Company("1234567-8")
        company.save()
        # There is no result called names3
        mock_service.save_data_to_db("names3", "order", [0], "name", Name,
                                     company)

        # Now database should not have any names
        result = Name.objects.all()
        self.assertEqual(0, len(result))

    def test_number_of_results(self):
        service = BusinessDataService()
        self.assertEqual(0, service.number_of_results())

    def test_empty_value_is_not_stored_to_db(self):
        mock_service = MockBusinessDataServiceWithEmptyPhoneNumber()

        company = Company("1234567-8")
        company.save()
        mock_service.save_data_to_db("contactDetails", "type",
                                     ["Matkapuhelin", "Mobiltelefon",
                                      "Mobile phone",
                                      "Puhelin", "Telefon", "Telephone"],
                                     "value", PhoneNumber, company)
        # Now database should not have empty phone number, but phone number
        # with value
        result = PhoneNumber.objects.all()
        self.assertEqual(1, len(result))
        self.assertEqual("+358501234567", result[0].value)

    def test_address_in_db_is_ended(self):
        self.populateDb()
        mock_service = MockBusinessDataService()
        company = Company("1234567-8")
        company.save()

        # mock_service.save_addresses_to_db(company)
        mock_service.save_data_to_db("addresses", "type", [1, 2], "street",
                                     Address, company,
                                     mock_service.get_address_from_db,
                                     mock_service.create_address)
        # Now Teststreet 1 should be ended with end date 2020-04-05
        address = Address.objects.filter(street="Test street 1")
        self.assertEqual(1, len(address))
        self.assertEqual("2020-04-05", str(address[0].end_date))

    def test_form_response_from_db(self):
        # First put some data to db
        self.populateDb()

        # Then form response and check that all fields are set
        service = BusinessDataService()
        response = service.form_response_from_db("1234567-8")
        self.assertEqual(response["business_id"], "1234567-8")
        self.assertEqual(response["name"], "Test company")
        self.assertEqual(response["address"], "Test street 1, 12345 Testcity")
        self.assertEqual(response["phone"], "1234567")
        self.assertEqual(response["website"], "www.testcompany.fi")

    def test_last_modified_result_is_selected(self):
        # First put some data to db
        company = self.populateDb()

        address = Address(street="Test street 2", post_code="12345",
                          city="Testcity", registration_date="2020-01-01",
                          language="FI", data_type="1", version="1",
                          end_date=None, company=company)
        address.save()

        # Then form response and check that Tests street 2 is the address
        service = BusinessDataService()
        response = service.form_response_from_db("1234567-8")
        self.assertEqual(response["address"], "Test street 2, 12345 Testcity")

    def test_form_response_without_data(self):
        # First put some data to db but don't include address
        self.populateDb(False)

        # Then form response and check that all fields are set
        service = BusinessDataService()
        response = service.form_response_from_db("1234567-8")
        self.assertEqual(response["business_id"], "1234567-8")
        self.assertEqual(response["name"], "Test company")
        self.assertEqual(response["address"], "")
        self.assertEqual(response["phone"], "")
        self.assertEqual(response["website"], "")

    def test_get_result_without_json_data(self):
        service = BusinessDataService()
        self.assertEqual(None, service.get_result())

    def populateDb(self, includeData=True):
        company = Company("1234567-8")
        company.save()
        name = Name(value="Test company", registration_date="2020-01-01",
                    end_date=None, company=company)
        name.save()
        if(includeData):
            address = Address(street="Test street 1", post_code="12345",
                              city="Testcity", registration_date="2020-01-01",
                              language="FI", data_type="1", version="1",
                              end_date=None, company=company)
            address.save()

            phone = PhoneNumber(value="1234567",
                                registration_date="2020-01-01",
                                end_date=None, company=company)
            phone.save()
            website = Website(value="www.testcompany.fi",
                              registration_date="2020-01-01",
                              end_date=None, company=company)
            website.save()
        return company


class MockBusinessDataService (BusinessDataService):

    def do_api_call(self):
        # Do nothing here
        pass

    def get_result(self):
        test_json_string = """
                {"businessId":"1234567-8",
                "name":"Nokia Oyj",
                "registrationDate":"1978-03-15",
                "companyForm":"OYJ","detailsUri":null,"liquidations":[],
                "names":[
                    {"order":0,"version":1,"name":"Nokia Oyj",
                    "registrationDate":"1997-09-01",
                    "endDate":null,"source":1},
                    {"order":0,"version":2,"name":"Oy Nokia Ab",
                    "registrationDate":"1966-06-10",
                    "endDate":"1997-08-31","source":1},
                    {"order":5,"version":1,
                    "name":"Nokia Abp",
                    "registrationDate":"1997-09-01","endDate":null,
                    "source":1},
                    {"order":6,"version":1,"name":"Nokia Corporation",
                    "registrationDate":"1997-09-01","endDate":null,"source":1}],
                "addresses":[
                    {"careOf":null,"street":"Karaportti 3",
                    "postCode":"02610","type":2,"version":2,"city":"ESPOO",
                    "country":null,
                    "version":"1","registrationDate":"2014-08-26"},
                    {"careOf":null,"street":"Test street 1",
                    "postCode":"12345","city":"Testcity",
                    "registrationDate":"2020-01-01",
                    "language":"FI",
                    "type":"1",
                    "version":"1",
                    "endDate":"2020-04-05"}]
                }
                """
        return json.loads(test_json_string)


class MockBusinessDataServiceWithEmptyPhoneNumber (BusinessDataService):

    def do_api_call(self):
        # Do nothing here
        pass

    def get_result(self):
        test_json_string = """
                {"businessId":"1234567-3",
                "name":"Company Oy",
                "contactDetails":[
                    {"version":1,"value":"","type":"Puhelin","registrationDate":"2013-03-10","endDate":null,"language":"FI","source":0},
                    {"version":1,"value":"","type":"Telefon","registrationDate":"2013-03-10","endDate":null,"language":"SE","source":0},
                    {"version":1,"value":"","type":"Telephone","registrationDate":"2013-03-10","endDate":null,"language":"EN","source":0},
                    {"version":1,"value":"+358501234567","type":"Matkapuhelin","registrationDate":"2013-04-15","endDate":null,"language":"FI","source":0},
                    {"version":2,"value":"+358417595482","type":"Puhelin","registrationDate":"2013-02-12","endDate":"2013-03-09","language":"FI","source":0}]
                }
                """
        return json.loads(test_json_string)
