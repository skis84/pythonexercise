from django.test import TestCase


from companies.validator import Validator
from companies.businessdataservice import BusinessDataService
import json
from .models import Company, Name, Address, PhoneNumber, Website


class ValidatorTestCase(TestCase):

    def test_valid_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("1805912-3"), True)

    def test_valid_business_id_old_6_numbers(self):
        self.assertEqual(Validator.is_valid_company_id("116510-6"), True)

    def test_invalid_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("18059123"), False)

    def test_invalid_checksum_in_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("0112039-9"), False)
        self.assertEqual(Validator.is_valid_company_id("1805912-1"), False)
        self.assertEqual(Validator.is_valid_company_id("1805912-0"), False)


class BusinessDataServiceTestCase(TestCase):

    def test_get_business_id(self):
        mock_service = MockBusinessDataService()
        mock_service.get_results("012345678")
        self.assertEqual(mock_service.get_business_id(), "0112038-9")

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

    def populateDb(self, includeData=True):
        company = Company("1234567-8")
        company.save()
        name = Name(value="Test company", registration_date="2020-01-01",
                    end_date=None, company=company)
        name.save()
        if(includeData):
            address = Address(street="Test street 1", post_code="12345",
                              city="Testcity", registration_date="2020-01-01",
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


class MockBusinessDataService (BusinessDataService):
    def get_results(self, company_id):
        test_json_string = """
                [{"businessId":"0112038-9",
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
                "registrationDate":"1997-09-01","endDate":null,"source":1}
                ],
                "addresses":[
                    {"careOf":null,"street":"Karaportti 3",
                    "postCode":"02610","type":2,"version":2,"city":"ESPOO",
                    "country":null,"registrationDate":"2014-08-26"}]
                }]
                """
        self.results = json.loads(test_json_string)
